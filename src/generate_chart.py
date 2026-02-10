"""
Thank you to Tobias Rodriguez del Pozo for his assistance in writing this code.
"""

from matplotlib import dates
import numpy as np
import pandas as pd

from pathlib import Path
from settings import config
import matplotlib.pyplot as plt

import plotly.graph_objects as go


OUTPUT_DIR = config("OUTPUT_DIR")
DATA_DIR = config("DATA_DIR")



def load_CRSP_monthly_stock_data(data_dir=DATA_DIR):
    path = Path(data_dir) / "CRSP_monthly_stock.parquet"
    df = pd.read_parquet(path)
    return df


def load_r30_day_T_bill(data_dir=DATA_DIR):
    path = Path(data_dir) / "CRSP_30_day_T_bill.parquet"
    df = pd.read_parquet(path)
    return df


def generate_chart(stock_market_return, T_bill):
    required_cols = {"date", "vwretd", "vwretx"}
    assert required_cols.issubset(stock_market_return.columns), \
        f"Missing columns: {required_cols - set(stock_market_return.columns)}"

    market = (
        stock_market_return[["date", "vwretd", "vwretx"]]
        .drop_duplicates(subset=["date"])
        .sort_values("date")
    )

    market = market.merge(T_bill[["date", "t30ret"]], on="date", how="left")
    market["excess_mkt"] = market["vwretd"] - market["t30ret"]

    outdir = Path(OUTPUT_DIR)
    outdir.mkdir(parents=True, exist_ok=True)

    # ---- Chart 1: market returns (2 lines)
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=market["date"], y=market["vwretd"], mode="lines",
                              name="VW Market Return (with distributions)"))
    fig1.add_trace(go.Scatter(x=market["date"], y=market["vwretx"], mode="lines",
                              name="VW Market Return (ex distributions)"))
    fig1.update_layout(
        title="CRSP Value-Weighted Market Returns",
        xaxis_title="Date",
        yaxis_title="Monthly Return",
        template="plotly_white",
    )
    fig1.write_html(outdir / "crsp_market_returns.html", include_plotlyjs="cdn")

    # ---- Chart 2: risk-free rate
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=market["date"], y=market["t30ret"], mode="lines",
                              name="30D T-bill"))
    fig2.update_layout(
        title="30-Day Treasury Bill Rate",
        xaxis_title="Date",
        yaxis_title="Monthly Risk-Free Rate",
        template="plotly_white",
        showlegend=False,
    )
    fig2.write_html(outdir / "crsp_30day_tbill.html", include_plotlyjs="cdn")

    # ---- Chart 3: excess returns
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=market["date"], y=market["excess_mkt"], mode="lines",
                              name="Excess Market Return"))
    fig3.update_layout(
        title="Excess Market Return",
        xaxis_title="Date",
        yaxis_title="Excess Return",
        template="plotly_white",
        showlegend=False,
    )
    fig3.write_html(outdir / "excess_market_return.html", include_plotlyjs="cdn")

    

if __name__ == "__main__":
    # Load CRSP monthly stock data
    stock_market_return = load_CRSP_monthly_stock_data(DATA_DIR)
    T_bill = load_r30_day_T_bill(DATA_DIR)
    generate_chart(stock_market_return, T_bill)
