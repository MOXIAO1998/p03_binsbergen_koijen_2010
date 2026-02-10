"""Run or update the project. This file uses the `doit` Python package. It works
like a Makefile, but is Python-based

"""

#######################################
## Configuration and Helpers for PyDoit
#######################################
## Make sure the src folder is in the path
import sys

sys.path.insert(1, "./src/")

import shutil
from os import environ
from pathlib import Path


DOIT_CONFIG = {"backend": "sqlite3", "dep_file": "./.doit-db.sqlite"}


BASE_DIR = Path("BASE_DIR")
DATA_DIR = Path("DATA_DIR")
MANUAL_DATA_DIR = Path("MANUAL_DATA_DIR")
OUTPUT_DIR = Path("OUTPUT_DIR")
OS_TYPE = Path("OS_TYPE")
USER = Path("USER")


##################################
## Begin PyDoit tasks here
##################################



def task_pull_CRSP_stock():
    return {
        'file_dep':[],
        'actions': ['python src/pull_CRSP_stock.py'],
        'targets':['_data/CRSP_monthly_stock.parquet']
    }

def task_pull_30_day_T_bill():
    return {
        'file_dep':[],
        'actions': ['python src/pull_30_day_T_bill.py'],
        'targets':['_data/CRSP_30_day_T_bill.parquet']
    }

def task_generate_chart():
    return {
        'file_dep':["_data/CRSP_monthly_stock.parquet",'_data/CRSP_30_day_T_bill.parquet'],
        'actions': ['python src/generate_chart.py'],
        'targets':['_output/crsp_market_returns.png','_output/crsp_30day_tbill.png','_output/excess_market_return.png']
    }