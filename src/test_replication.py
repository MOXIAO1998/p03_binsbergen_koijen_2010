from pathlib import Path

import pytest

from misc_tools import (
    data_loader_divident_growth_stats,
    data_loader_ols_predictive_regressions,
    data_loader_market_reinvested_dividend_growth,
)


from settings import (
    EXPECTATION_TABLE1,
    EXPECTATION_TABLE3,
    EXPECTATION_TABLE4
)
from settings import config
DATA_DIR = Path(config("DATA_DIR"))
OUTPUT_DIR = Path(config("OUTPUT_DIR"))

def assert_nested_dict_close(
actual: dict,
expected: dict,
rel_tol: float = 0.05,
abs_tol: float = 1e-3,
) -> None:
    for col in expected:
        assert col in actual, f"Missing column in actual output: {col}"

        for row in expected[col]:
            assert row in actual[col], f"Missing row '{row}' under column '{col}'"

            exp_val = expected[col][row]
            act_val = actual[col][row]

            assert act_val == pytest.approx(exp_val, rel=rel_tol, abs=abs_tol), (
                f"{col} - {row} failed: expected {exp_val}, got {act_val}"
            )


def test_dividend_growth_stats_matches_reference_table():
    csv_path = OUTPUT_DIR / "dividend_growth_stats.csv"
    actual = data_loader_divident_growth_stats(csv_path)

    assert_nested_dict_close(actual=actual, expected=EXPECTATION_TABLE1, rel_tol=0.1, abs_tol=1e-3)


def test_ols_predictive_regressions():
    csv_path = OUTPUT_DIR / "OLS_predictive_regressions.csv"
    actual = data_loader_ols_predictive_regressions(csv_path)
    
    assert_nested_dict_close(actual=actual, expected=EXPECTATION_TABLE3, rel_tol=0.1, abs_tol=1e-3)


def test_specs_for_market_reinvested_dividend_growth():
    csv_path = OUTPUT_DIR / "specs_for_market_reinvested_dividend_growth.csv"
    actual = data_loader_market_reinvested_dividend_growth(csv_path)

    assert_nested_dict_close(actual=actual, expected=EXPECTATION_TABLE4, rel_tol=0.3, abs_tol=2e-2)