from enum import Enum
from typing import Optional
from pathlib import Path
from pydantic import BaseModel, Field
import anywidget
import traitlets


class SeriesType(str, Enum):
    CANDLESTICK = "candlestick"
    LINE = "line"
    HISTOGRAM = "histogram"


class SeriesStyle(BaseModel):
    color: str = ""
    up_color: str = "#26a69a"
    down_color: str = "#ef5350"
    border_visible: bool = False
    wick_up_color: str = "#26a69a"
    wick_down_color: str = "#ef5350"

    class Config:
        alias_generator = lambda s: "".join(
            word.capitalize() if i else word for i, word in enumerate(s.split("_"))
        )


class TimeScaleConfig(BaseModel):
    visible: bool = True
    time_visible: bool = True
    seconds_visible: bool = True


class LayoutConfig(BaseModel):
    background: dict[str, str] = Field(
        default_factory=lambda: {"type": "solid", "color": "white"}
    )
    text_color: str = "black"

    class Config:
        alias_generator = lambda s: "textColor" if s == "text_color" else s


class ChartConfig(BaseModel):
    width: int = 600
    height: int = 400
    layout: LayoutConfig = Field(default_factory=LayoutConfig)
    time_scale: TimeScaleConfig = Field(default_factory=TimeScaleConfig)


class SeriesConfig(BaseModel):
    id: str
    type: SeriesType
    style: SeriesStyle
    data: list[dict] = Field(default_factory=list)


class Series:
    def __init__(self, series_id: str, series_type: SeriesType, style: SeriesStyle, chart: 'TradingChart'):
        self.id = series_id
        self.type = series_type
        self.style = style
        self.chart = chart
        self.data = []

    def set_data(self, data: list[dict]):
        self.data = data
        self.chart._update_series_configs()

    def update_data(self, data_point: dict):
        self.data.append(data_point)
        self.chart._update_series_configs()

    def to_config(self) -> SeriesConfig:
        return SeriesConfig(
            id=self.id, type=self.type, style=self.style, data=self.data
        )


class TradingChart(anywidget.AnyWidget):
    _config = traitlets.Dict({}).tag(sync=True)
    _series_configs = traitlets.List([]).tag(sync=True)

    def __init__(self, _config: dict, _esm: str, _css: str = ""):
        super().__init__(_config=_config, _esm=_esm, _css=_css)
        self._series: dict[str, Series] = {}

    @staticmethod
    def create(config: ChartConfig) -> "TradingChart":
        assets_dir = Path(__file__).parent.parent / "assets"
        cdn_import = "import 'https://unpkg.com/lightweight-charts@4.2.2/dist/lightweight-charts.standalone.production.js';\n"
        template_path = assets_dir / "chart_template.js"
        if not template_path.exists():
            raise FileNotFoundError(
                f"Required JavaScript file not found: {template_path}"
            )
        return TradingChart(
            _config=config.model_dump(by_alias=True),
            _esm=cdn_import + template_path.read_text(),
        )

    def add_candlestick_series(self, style: Optional[SeriesStyle] = None) -> Series:
        style = style or SeriesStyle()
        series_id = f"candlestick_{len(self._series)}"
        series = Series(series_id, SeriesType.CANDLESTICK, style, self)
        self._series[series_id] = series
        self._update_series_configs()
        return series

    def add_line_series(self, color: str) -> Series:
        style = SeriesStyle(color=color)
        series_id = f"line_{len(self._series)}"
        series = Series(series_id, SeriesType.LINE, style, self)
        self._series[series_id] = series
        self._update_series_configs()
        return series

    def add_histogram_series(
        self,
        price_format: dict = {"type": "volume"},
        scale_margins: dict = {"top": 0.7, "bottom": 0},
    ) -> Series:
        series_id = f"histogram_{len(self._series)}"
        series = Series(series_id, SeriesType.HISTOGRAM, SeriesStyle(), self)
        self._series[series_id] = series
        self._update_series_configs()
        return series

    def _update_series_configs(self):
        configs = [
            series.to_config().model_dump(by_alias=True)
            for series in self._series.values()
        ]
        self._series_configs = configs
