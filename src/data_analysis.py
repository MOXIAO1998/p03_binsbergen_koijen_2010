from pathlib import Path
import pandas as pd
from settings import config
DATA_DIR = Path(config("DATA_DIR"))
WRDS_USERNAME = config("WRDS_USERNAME")
START_DATE = config("START_DATE")
END_DATE = config("END_DATE")

def load_CRSP_monthly_file(data_dir=DATA_DIR):
    path = Path(data_dir) / "CRSP_monthly_stock_to_2007.parquet"
    df = pd.read_parquet(path)
    return df

def load_CRSP_30_day_T_bill(data_dir=DATA_DIR):
    path = Path(data_dir) / "CRSP_30_day_T_bill_to_2007.parquet"
    df = pd.read_parquet(path)
    return df


def main():
    stock = load_CRSP_monthly_file()
    Tbill = load_CRSP_30_day_T_bill()
    print(stock.head(5))
    print(Tbill.head(5))



if __name__ == "__main__":
    main()