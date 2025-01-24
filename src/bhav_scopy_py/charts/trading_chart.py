import json
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4

import anywidget
import traitlets
from pydantic import BaseModel, Field


class ChartConfig(BaseModel):
    width: int = 600
    height: int = 400
    layout: dict = Field(
        default_factory=lambda: {
            "background": {"type": "solid", "color": "white"},
            "textColor": "black",
        }
    )
    timeScale: dict = Field(
        default_factory=lambda: {
            "visible": True,
            "timeVisible": True,
            "secondsVisible": True,
        }
    )


class Series:
    def __init__(self, series_id: str, chart: "TradingChart"):
        self.id = series_id
        self.chart = chart

    def setData(self, data: list[dict]):
        js_call = f"series.get('{self.id}').setData({json.dumps(data)});"
        self.chart._add_js_call(js_call)

    def setMarkers(self, markers: list[dict]):
        js_call = f"series.get('{self.id}').setMarkers({json.dumps(markers)});"
        self.chart._add_js_call(js_call)


class TradingChart(anywidget.AnyWidget):
    _js_calls = traitlets.List([]).tag(sync=True)
    _config = traitlets.Dict({}).tag(sync=True)

    def __init__(self, config: Optional[ChartConfig] = None):
        assets_dir = Path(__file__).parent.parent / "assets"
        js_path = assets_dir / "chart_template.js"

        if not config:
            config = ChartConfig()

        super().__init__(
            _esm=f"import 'https://unpkg.com/lightweight-charts@4.2.2/dist/lightweight-charts.standalone.production.js';\n"
            + js_path.read_text(),
            _config=config.model_dump(by_alias=True),
            _js_calls=[],
        )

    def _add_js_call(self, js_call: str):
        self._js_calls = [*self._js_calls, js_call]

    def addCandlestickSeries(self, options: Optional[dict] = None) -> Series:
        series_id = f"series_{uuid4().hex[:8]}"
        js_call = f"series.set('{series_id}', chart.addCandlestickSeries({json.dumps(options or {})}));"
        self._add_js_call(js_call)
        return Series(series_id, self)

    def addLineSeries(self, options: Optional[dict] = None) -> Series:
        series_id = f"series_{uuid4().hex[:8]}"
        js_call = f"series.set('{series_id}', chart.addLineSeries({json.dumps(options or {})}));"
        self._add_js_call(js_call)
        return Series(series_id, self)

    def addHistogramSeries(self, options: Optional[dict] = None) -> Series:
        series_id = f"series_{uuid4().hex[:8]}"
        js_call = f"series.set('{series_id}', chart.addHistogramSeries({json.dumps(options or {})}));"
        self._add_js_call(js_call)
        return Series(series_id, self)
