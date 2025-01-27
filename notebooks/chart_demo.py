# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.6
#   kernelspec:
#     display_name: .venv (3.10.15)
#     language: python
#     name: python3
# ---

from datetime import datetime, timedelta

import numpy as np

from bhav_scopy_py.charts.trading_chart import ChartConfig, TradingChart


def generate_sample_data(n_periods=100, start_price=100, volatility=0.02):
    np.random.seed(42)
    dates = [datetime.now() - timedelta(days=x) for x in range(n_periods)]
    dates.reverse()

    prices = [start_price]
    for _ in range(n_periods - 1):
        change = np.random.normal(0, volatility)
        prices.append(prices[-1] * (1 + change))

    data = []
    for i, date in enumerate(dates):
        base_price = prices[i]
        high = base_price * (1 + abs(np.random.normal(0, volatility / 2)))
        low = base_price * (1 - abs(np.random.normal(0, volatility / 2)))
        open_price = np.random.uniform(low, high)
        close_price = np.random.uniform(low, high)
        volume = np.random.randint(1000, 10000)

        data.append(
            {
                "time": date.strftime("%Y-%m-%d"),
                "open": float(open_price),
                "high": float(high),
                "low": float(low),
                "close": float(close_price),
                "volume": float(volume),
            }
        )

    return data


config = ChartConfig(
    width=800,
    height=600,
    layout={"background": {"type": "solid", "color": "white"}, "textColor": "black"},
)
chart = TradingChart(config)

candlestick_series = chart.add_candlestick_series({
    "upColor": "#26a69a",
    "downColor": "#ef5350",
    "wickUpColor": "#26a69a",
    "wickDownColor": "#ef5350",
})

volume_series = chart.add_histogram_series({
    "color": "#26a69a"
})

data = generate_sample_data()

candlestick_series.set_data(data)

volume_data = [
    {
        "time": d["time"],
        "value": d["volume"],
        "color": "#26a69a" if d["close"] > d["open"] else "#ef5350",
    }
    for d in data
]
volume_series.set_data(volume_data)

# Display chart
chart


