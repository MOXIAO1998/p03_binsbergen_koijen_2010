"""
Functions to pull and calculate the value and equal weighted CRSP indices.

This module uses the CRSP CIZ format (Flat File Format 2.0), which replaced
the legacy SIZ format as of January 2025.

Key resources:
 - Data for indices: https://wrds-www.wharton.upenn.edu/data-dictionary/crsp_a_indexes/
 - Tidy Finance guide: https://www.tidy-finance.org/python/wrds-crsp-and-compustat.html
 - CRSP 2.0 Update: https://www.tidy-finance.org/blog/crsp-v2-update/
 - Transition FAQ: https://wrds-www.wharton.upenn.edu/pages/support/manuals-and-overviews/crsp/stocks-and-indices/crsp-stock-and-indexes-version-2/crsp-ciz-faq/
 - Cross-Reference Guide: https://www.crsp.org/wp-content/uploads/guides/CRSP_Cross_Reference_Guide_1.0_to_2.0.pdf

Key changes from SIZ to CIZ format:
 - Monthly stock table: crspm.msf -> crspm.msf_v2
 - Security info: crspm.msenames -> crspm.stksecurityinfohist
 - Delisting returns are now built into mthret (no separate table needed)
 - Column names: date->mthcaldt, ret->mthret, retx->mthretx, prc->mthprc
 - Share code filters (shrcd) replaced with securitytype, securitysubtype, sharetype

Thank you to Tobias Rodriguez del Pozo for his assistance in writing this code.

"""

from pathlib import Path

import pandas as pd
import wrds


from settings import config

DATA_DIR = Path(config("DATA_DIR"))
WRDS_USERNAME = config("WRDS_USERNAME")
START_DATE = config("START_DATE")
END_DATE = config("END_DATE")


from datetime import datetime
import wrds
import pandas as pd


def pull_30_day_T_bill(
    start_date="1946-01-01",
    end_date="2007-12-31",
    wrds_username=WRDS_USERNAME,
):
    """
    Pull CRSP 30-day T-bill returns (t30ret)
    using CRSP CIZ 2.0 (wrds_msfv2_query).

    Returns
    -------
    DataFrame with:
        - mthcaldt
        - t30ret
    """

    query = f"""
        SELECT
           mcti.caldt AS date,
           mcti.t30ret AS t30ret
        FROM crspm.mcti AS mcti
        
        WHERE
            mcti.caldt BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY mcti.caldt
    """

    db = wrds.Connection(wrds_username=wrds_username)
    df = db.raw_sql(query, date_cols=["date"])
    db.close()

    return df



def load_CRSP_30_day_T_bill(data_dir=DATA_DIR):
    path = Path(data_dir) / "CRSP_30_day_T_bill.parquet"
    df = pd.read_parquet(path)
    return df




if __name__ == "__main__":
    df_msf = pull_30_day_T_bill(start_date=START_DATE, end_date=END_DATE, wrds_username=WRDS_USERNAME)
    path = Path(DATA_DIR) / "CRSP_30_day_T_bill.parquet"
    path.parent.mkdir(parents=True, exist_ok=True)
    df_msf.to_parquet(path)

