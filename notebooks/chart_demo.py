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
import pandas as pd

from bhav_scopy_py.charts.trading_chart import ChartConfig, TradingChart


def generate_sample_ohlc(n_periods=100, start_price=100, volatility=0.02):
    np.random.seed(42)  # For reproducibility
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

        data.append(
            {
                "time": date.strftime("%Y-%m-%d"),
                "open": float(open_price),
                "high": float(high),
                "low": float(low),
                "close": float(close_price),
            }
        )

    return data


sample_data = generate_sample_ohlc()
chart = TradingChart.create(ChartConfig(width=800, height=500))
chart._chart_data = sample_data
chart
