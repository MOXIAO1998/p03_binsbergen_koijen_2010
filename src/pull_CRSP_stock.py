"""
Functions to pull and calculate the value and equal weighted CRSP indices.

This module uses the CRSP CIZ format (Flat File Format 2.0), which replaced
the legacy SIZ format as of January 2025.

Key resources:
 - Data for indices: https://wrds-www.wharton.upenn.edu/data-dictionary/crsp_m_stock/
 - Tidy Finance guide: https://www.tidy-finance.org/python/wrds-crsp-and-compustat.html
 - CRSP 2.0 Update: https://www.tidy-finance.org/blog/crsp-v2-update/
 - Transition FAQ: https://wrds-www.wharton.upenn.edu/pages/support/manuals-and-overviews/crsp/stocks-and-indices/crsp-stock-and-indexes-version-2/crsp-ciz-faq/
 - Cross-Reference Guide: https://www.crsp.org/wp-content/uploads/guides/CRSP_Cross_Reference_Guide_1.0_to_2.0.pdf

Key changes from SIZ to CIZ format:
 - Monthly stock table: crspm.msf -> crspm.wrds_msfv2_query
 - Security info: crspm.msenames -> crspm.stksecurityinfohist
 - Delisting returns are now built into mthret (no separate table needed)
 - Column names: date->mthcaldt, vwretd->vwretd, vwretx->vwretx
 - Share code filters (shrcd) replaced with securitytype, securitysubtype, sharetype


https://wrds-www.wharton.upenn.edu/pages/get-data/center-research-security-prices-crsp/monthly-update/stock-version-2/monthly-stock-file/
"""

from pathlib import Path
import wrds


from settings import config

DATA_DIR = Path(config("DATA_DIR"))
WRDS_USERNAME = config("WRDS_USERNAME")
START_DATE = config("START_DATE")
END_DATE = config("END_DATE")



def pull_CRSP_monthly_file(
    start_date,
    end_date,
    wrds_username,
):
    """
    Pull CRSP value-weighted index returns (VWRETD, VWRETX)
    for NYSE / AMEX / NASDAQ (primaryexch = N, A, Q)
    using CRSP CIZ 2.0 (wrds_msfv2_query).

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
                DISTINCT msf.mthcaldt AS date,
                msf.vwretd AS vwretd,
                msf.vwretx AS vwretx
            FROM crspm.wrds_msfv2_query AS msf
            
            WHERE
                msf.mthcaldt >= '{start_date}'
                AND msf.primaryexch IN ('N', 'A', 'Q')
            ORDER BY msf.mthcaldt
         """

    else:
        query = f"""
            SELECT
                DISTINCT msf.mthcaldt AS date,
                msf.vwretd AS vwretd,
                msf.vwretx AS vwretx
            FROM crspm.wrds_msfv2_query AS msf
            
            WHERE
                msf.mthcaldt BETWEEN '{start_date}' AND '{end_date}'
                AND msf.primaryexch IN ('N', 'A', 'Q')
            ORDER BY msf.mthcaldt
        """

    db = wrds.Connection(wrds_username=wrds_username)
    df = db.raw_sql(query, date_cols=["date"])
    db.close()

    return df

if __name__ == "__main__":
    df_msf = pull_CRSP_monthly_file(start_date=START_DATE, end_date=END_DATE, wrds_username=WRDS_USERNAME)
    path = Path(DATA_DIR) / "CRSP_monthly_stock_44_to_07.parquet"
    path.parent.mkdir(parents=True, exist_ok=True)
    df_msf.to_parquet(path)


    df_msf = pull_CRSP_monthly_file(start_date=START_DATE, end_date=None, wrds_username=WRDS_USERNAME)
    path = Path(DATA_DIR) / "CRSP_monthly_stock_44_to_latest.parquet"
    path.parent.mkdir(parents=True, exist_ok=True)
    df_msf.to_parquet(path)

