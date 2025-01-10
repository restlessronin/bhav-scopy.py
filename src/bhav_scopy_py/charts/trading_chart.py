from dataclasses import dataclass
from pathlib import Path

import anywidget
import traitlets


@dataclass(frozen=True)
class ChartConfig:
    width: int = 600
    height: int = 400


class TradingChart(anywidget.AnyWidget):
    _chart_data = traitlets.List([]).tag(sync=True)
    _config = traitlets.Dict({}).tag(sync=True)

    def __init__(self, _config: dict, _esm: str, _css: str = ""):
        super().__init__(_config=_config, _esm=_esm, _css=_css)

    @staticmethod
    def create(config: ChartConfig) -> "TradingChart":
        assets_dir = Path(__file__).parent.parent / "assets"
        cdn_import = "import 'https://unpkg.com/lightweight-charts@4.2.2/dist/lightweight-charts.standalone.production.js';\n"
        template_path = assets_dir / "chart_template.js"
        if not template_path.exists():
            raise FileNotFoundError(
                f"Required JavaScript file not found: {template_path}"
            )
        chart_config = config
        base_config = {
            "width": chart_config.width,
            "height": chart_config.height,
            "layout": {"background": {"color": "#ffffff"}, "textColor": "#333"},
        }
        return TradingChart(
            _config=base_config, _esm=cdn_import + template_path.read_text()
        )
