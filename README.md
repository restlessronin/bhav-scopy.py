# bhav-scopy.py

A Python library for creating interactive trading charts in Jupyter notebooks, built on lightweight-charts. Features include:

- Candlestick charts with customizable styling
- Volume histograms with color coding
- Simple API for chart creation and data updates
- Responsive sizing and layout

## Installation
```uv pip install bhav-scopy.py```

## Basic Usage
```python
from bhav_scopy_py.charts.trading_chart import ChartConfig, TradingChart

# Create chart
config = ChartConfig(width=800, height=600)
chart = TradingChart(config)

# Add candlestick series
series = chart.addCandlestickSeries()
series.setData(ohlcv_data)  # List of dicts with time, open, high, low, close
```
