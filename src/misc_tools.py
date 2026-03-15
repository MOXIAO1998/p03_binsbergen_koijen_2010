"""Collection of miscelaneous tools useful in a variety of situations
(not specific to the current project)
"""

from pathlib import Path
import pandas as pd
from settings import (
    EXPECTATION_TABLE1
)


########################################################################################
## Pandas Helpers
########################################################################################

def data_loader_divident_growth_stats(csv_path: Path):
    """
        read csv data to pd
    """
    df = pd.read_csv(csv_path, index_col=0)

    df.index = df.index.str.strip()
    df.columns = df.columns.str.strip()

    actual = {
        col: {row: float(df.loc[row, col]) for row in df.index}
        for col in df.columns
    }
    return actual




def data_loader_ols_predictive_regressions(csv_path: Path) -> dict:
    """
    Load OLS predictive regression summary statistics from a CSV file.

    Expected CSV format:
        first column: row labels
        remaining columns: regression result columns, e.g.
            r_M, r, delta_d_M, delta_d

    Returns
    -------
    dict
        Nested dictionary of the form:
        {
            "r_M": {
                "Constant": 0.4572,
                "SE(Constant)": 0.1541,
                ...
            },
            ...
        }
    """
    df = pd.read_csv(csv_path, index_col=0)

    # 
    df.index = df.index.astype(str).str.strip()
    df.columns = df.columns.astype(str).str.strip()

    df = df.astype(float)

    result = {
        col: {row: float(df.loc[row, col]) for row in df.index}
        for col in df.columns
    }

    return result







def data_loader_market_reinvested_dividend_growth(csv_path: str | Path) -> dict:
    """
    Load market reinvested dividend growth specification results from CSV.

    Expected CSV format:
    - First column contains row labels
    - Remaining columns are model specifications
    - Empty cells are allowed and will be skipped

    Returns
    -------
    dict
        Nested dictionary like:
        {
            "AR1": {
                "Constant": 0.0721,
                "SE(Constant)": 0.0171,
                ...
            },
            "r_lag_only": {...},
            "ARMAX1_r_lag": {...},
        }
    """
    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    df = pd.read_csv(csv_path, index_col=0)

    df.index = df.index.astype(str).str.strip()
    df.columns = df.columns.astype(str).str.strip()

    result = {}
    for col in df.columns:
        result[col] = {}
        for row in df.index:
            value = df.loc[row, col]

            if pd.isna(value) or str(value).strip() == "":
                continue

            result[col][row] = float(value)

    return result