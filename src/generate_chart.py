"""
generate chart and table of replication
"""

import base64
import pandas as pd
import numpy as np
import math
import statsmodels.api as sm
from scipy.optimize import minimize
from statsmodels.tools.numdiff import approx_hess
import matplotlib.pyplot as plt
from pathlib import Path
from settings import config

OUTPUT_DIR = Path(config("OUTPUT_DIR"))

tbill_df = pd.read_parquet("_data/CRSP_30_day_T_bill_44_to_07.parquet")
ret_df = pd.read_parquet("_data/CRSP_monthly_stock_44_to_07.parquet")
construction_start = "1944-01"

tbill_df_latest = pd.read_parquet("_data/CRSP_30_day_T_bill_44_to_latest.parquet")
ret_df_latest = pd.read_parquet("_data/CRSP_monthly_stock_44_to_latest.parquet")


def future_prod_excl_current(x):
    return x.iloc[::-1].cumprod().iloc[::-1].shift(-1, fill_value=1.0)


def monthly_annual(ret_df, tbill_df, end_year=2007):

    ret = ret_df.copy()
    rf = tbill_df.copy()

    ret.loc[:, "date"] = pd.to_datetime(ret["date"])
    rf.loc[:, "date"] = pd.to_datetime(rf["date"])

    ret.loc[:, "ym"] = ret["date"].dt.to_period("M")
    rf.loc[:, "ym"] = rf["date"].dt.to_period("M")

    monthly = (
        ret[["ym", "vwretd", "vwretx"]]
        .merge(rf[["ym", "t30ret"]], on="ym", how="inner")
        .sort_values("ym")
        .reset_index(drop=True)
    )

    start_period = pd.Period(construction_start, "M")
    end_period = pd.Period(f"{end_year}-12", "M")

    monthly = monthly[
        (monthly["ym"] >= start_period) &
        (monthly["ym"] <= end_period)
    ].copy()

    monthly.loc[:, "year"] = monthly["ym"].dt.year

    monthly.loc[:, "gross_mkt"] = 1.0 + monthly["vwretd"]
    monthly.loc[:, "gross_x"] = 1.0 + monthly["vwretx"]
    monthly.loc[:, "gross_rf"] = 1.0 + monthly["t30ret"]

    monthly.loc[:, "P_end"] = monthly["gross_x"].cumprod()
    monthly.loc[:, "P_beg"] = monthly["P_end"].shift(fill_value=1.0)

    monthly.loc[:, "div_month"] = monthly["P_beg"] * (
        monthly["vwretd"] - monthly["vwretx"]
    )

    monthly.loc[:, "to_ye_rf"] = monthly.groupby("year")[
        "gross_rf"
    ].transform(future_prod_excl_current)

    monthly.loc[:, "to_ye_mkt"] = monthly.groupby("year")[
        "gross_mkt"
    ].transform(future_prod_excl_current)

    monthly.loc[:, "div_cash_piece"] = (
        monthly["div_month"] * monthly["to_ye_rf"]
    )

    monthly.loc[:, "div_market_piece"] = (
        monthly["div_month"] * monthly["to_ye_mkt"]
    )

    annual_div = (
        monthly.groupby("year", as_index=False)[
            ["div_cash_piece", "div_market_piece"]
        ]
        .sum()
        .rename(columns={
            "div_cash_piece": "D_cash",
            "div_market_piece": "D_market"
        })
    )

    annual_price = (
        monthly.groupby("year", as_index=False)["P_end"]
        .last()
        .rename(columns={"P_end": "P"})
    )

    annual = (
        annual_price
        .merge(annual_div, on="year", how="inner")
        .sort_values("year")
        .reset_index(drop=True)
    )

    annual.loc[:, "delta_d"] = np.log(
        annual["D_cash"] / annual["D_cash"].shift(1)
    )

    annual.loc[:, "delta_d_M"] = np.log(
        annual["D_market"] / annual["D_market"].shift(1)
    )

    annual.loc[:, "r"] = np.log(
        (annual["P"] + annual["D_cash"]) / annual["P"].shift(1)
    )

    annual.loc[:, "r_M"] = np.log(
        (annual["P"] + annual["D_market"]) / annual["P"].shift(1)
    )

    annual.loc[:, "pd"] = np.log(annual["P"] / annual["D_cash"])
    annual.loc[:, "pd_M"] = np.log(annual["P"] / annual["D_market"])

    return monthly, annual


def replicate_table1(annual, start_year=1946, end_year=2007):

    growth = annual[
        (annual["year"] >= start_year) &
        (annual["year"] <= end_year)
    ].dropna(subset=["delta_d", "delta_d_M"]).copy()

    table1 = pd.DataFrame({
        "delta_d_M": growth["delta_d_M"].agg(
            ["mean", "median", "std", "max", "min"]
        ),
        "delta_d": growth["delta_d"].agg(
            ["mean", "median", "std", "max", "min"]
        ),
    })

    table1.index = [
        "Mean",
        "Median",
        "Standard deviation",
        "Maximum",
        "Minimum"
    ]

    return growth, table1


def run_ols(annual, y_col, pd_col, start_year=1946, end_year=2007):

    reg = annual[["year", y_col, pd_col]].copy()

    reg.loc[:, "pd_lag"] = reg[pd_col].shift(1)

    reg = reg[
        (reg["year"] >= start_year) &
        (reg["year"] <= end_year)
    ].copy()

    reg.loc[:, y_col] = pd.to_numeric(reg[y_col], errors="coerce")
    reg.loc[:, "pd_lag"] = pd.to_numeric(reg["pd_lag"], errors="coerce")

    reg = reg.replace([np.inf, -np.inf], np.nan).dropna()

    X = sm.add_constant(reg["pd_lag"].astype(float))

    model = sm.OLS(
        reg[y_col].astype(float),
        X
    ).fit()

    return {
        "model": model,
        "reg_df": reg,
        "n": int(model.nobs),
        "const": model.params["const"],
        "const_se": model.bse["const"],
        "beta": model.params["pd_lag"],
        "beta_se": model.bse["pd_lag"],
        "r2": model.rsquared,
        "adj_r2": model.rsquared_adj,
    }


def replicate_table3(annual, start_year=1946, end_year=2007):

    res_rM = run_ols(annual, "r_M", "pd_M", start_year, end_year)
    res_r = run_ols(annual, "r", "pd", start_year, end_year)
    res_dM = run_ols(annual, "delta_d_M", "pd_M", start_year, end_year)
    res_d = run_ols(annual, "delta_d", "pd", start_year, end_year)

    table3 = pd.DataFrame({
        "r_M": [
            res_rM["const"], res_rM["const_se"],
            res_rM["beta"], res_rM["beta_se"],
            res_rM["r2"], res_rM["adj_r2"],
        ],
        "r": [
            res_r["const"], res_r["const_se"],
            res_r["beta"], res_r["beta_se"],
            res_r["r2"], res_r["adj_r2"],
        ],
        "delta_d_M": [
            res_dM["const"], res_dM["const_se"],
            res_dM["beta"], res_dM["beta_se"],
            res_dM["r2"], res_dM["adj_r2"],
        ],
        "delta_d": [
            res_d["const"], res_d["const_se"],
            res_d["beta"], res_d["beta_se"],
            res_d["r2"], res_d["adj_r2"],
        ],
    })

    return table3, {
        "r_M": res_rM["model"],
        "r": res_r["model"],
        "delta_d_M": res_dM["model"],
        "delta_d": res_d["model"],
    }


def replicate_table4(annual, start_year=1946, end_year=2007):

    reg = annual[["year", "delta_d_M", "r"]].copy()

    reg.loc[:, "delta_d_M"] = pd.to_numeric(reg["delta_d_M"], errors="coerce")
    reg.loc[:, "r"] = pd.to_numeric(reg["r"], errors="coerce")

    reg.loc[:, "dM_lag"] = reg["delta_d_M"].shift(1)
    reg.loc[:, "r_lag"] = reg["r"].shift(1)

    reg = reg[
        (reg["year"] >= start_year) &
        (reg["year"] <= end_year)
    ].dropna()

    X1 = sm.add_constant(reg["dM_lag"].astype(float))
    m1 = sm.OLS(reg["delta_d_M"].astype(float), X1).fit()

    X2 = sm.add_constant(reg["r_lag"].astype(float))
    m2 = sm.OLS(reg["delta_d_M"].astype(float), X2).fit()

    table4 = pd.DataFrame({
        "AR1": [
            m1.params["const"],
            m1.bse["const"],
            m1.params["dM_lag"],
            m1.bse["dM_lag"],
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            m1.rsquared,
            m1.rsquared_adj,
        ],
        "r_lag_only": [
            m2.params["const"],
            m2.bse["const"],
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            m2.params["r_lag"],
            m2.bse["r_lag"],
            m2.rsquared,
            m2.rsquared_adj,
        ],
    })

    return reg, table4, {"col1": m1, "col2": m2}


def main():

    monthly, annual = monthly_annual(
        ret_df,
        tbill_df,
        end_year=2007
    )

    growth, table1 = replicate_table1(annual)
    table3, models3 = replicate_table3(annual)
    reg4, table4, models4 = replicate_table4(annual)

    (table1.round(4)).to_csv(
        OUTPUT_DIR / "dividend_growth_stats_2007.csv"
    )

    (table3.round(4)).to_csv(
        OUTPUT_DIR / "OLS_predictive_regressions_2007.csv"
    )

    (table4.round(4)).to_csv(
        OUTPUT_DIR / "specs_for_market_reinvested_dividend_growth_2007.csv"
    )


if __name__ == "__main__":
    main()