"""
Functions to pull and calculate the value and equal weighted CRSP indices.

This module uses the CRSP CIZ format (Flat File Format 2.0), which replaced
the legacy SIZ format as of January 2025.

Key resources:
 - Data for indices: https://wrds-www.wharton.upenn.edu/data-dictionary/crsp_m_indexes/
 - Tidy Finance guide: https://www.tidy-finance.org/python/wrds-crsp-and-compustat.html
 - CRSP 2.0 Update: https://www.tidy-finance.org/blog/crsp-v2-update/
 - Transition FAQ: https://wrds-www.wharton.upenn.edu/pages/support/manuals-and-overviews/crsp/stocks-and-indices/crsp-stock-and-indexes-version-2/crsp-ciz-faq/
 - Cross-Reference Guide: https://www.crsp.org/wp-content/uploads/guides/CRSP_Cross_Reference_Guide_1.0_to_2.0.pdf

Key changes from SIZ to CIZ format:
 - Monthly stock table: msp500 -> crspm.msp500
 - Security info: crspm.msenames -> crspm.stksecurityinfohist
 - Delisting returns are now built into mthret (no separate table needed)
 - Column names: date->caldt, sprtrn->sprtrn, spindx->spindx
 - Share code filters (shrcd) replaced with securitytype, securitysubtype, sharetype

"""

from pathlib import Path
import wrds

from settings import config

DATA_DIR = Path(config("DATA_DIR"))
WRDS_USERNAME = config("WRDS_USERNAME")
START_DATE = config("START_DATE")
END_DATE = config("END_DATE")


def pull_CRSP_SP500_file(
    start_date,
    end_date,
    wrds_username,
):
    """
    Pull CRSP Return and Level on SP composite index (sprtrn,spindx)

    Returns
    -------
    DataFrame with:
        - mthcaldt
        - vwretd
        - vwretx
    """
    if end_date is None:
        query = f"""
            SELECT
                DISTINCT sp500.caldt AS date,
                sp500.sprtrn AS sprtrn,
                sp500.spindx AS spindx
            FROM crspm.msp500 AS sp500
            
            WHERE
                sp500.caldt >= '{start_date}'
            ORDER BY sp500.caldt
        """

    else:
        query = f"""
            SELECT
                DISTINCT sp500.caldt AS date,
                sp500.sprtrn AS sprtrn,
                sp500.spindx AS spindx
            FROM crspm.msp500 AS sp500
            
            WHERE
                sp500.caldt BETWEEN '{start_date}' AND '{end_date}'
            ORDER BY sp500.caldt
        """

    db = wrds.Connection(wrds_username=wrds_username)
    df = db.raw_sql(query, date_cols=["date"])
    db.close()

    return df


if __name__ == "__main__":
    df_msf = pull_CRSP_SP500_file(start_date=START_DATE, end_date=END_DATE, wrds_username=WRDS_USERNAME)
    path = Path(DATA_DIR) / "CRSP_SP500_44_to_07.parquet"
    path.parent.mkdir(parents=True, exist_ok=True)
    df_msf.to_parquet(path)

    df_msf = pull_CRSP_SP500_file(start_date=START_DATE, end_date=None, wrds_username=WRDS_USERNAME)
    path = Path(DATA_DIR) / "CRSP_SP500_44_to_latest.parquet"
    path.parent.mkdir(parents=True, exist_ok=True)
    df_msf.to_parquet(path)


