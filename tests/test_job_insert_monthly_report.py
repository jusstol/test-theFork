# coding: utf-8

# Generic libs.
import pandas as pd
import pytest
import sys
from os.path import join, dirname, realpath
from sqlalchemy.exc import OperationalError

# Project modules to test.
sys.path.insert(0, join(dirname(realpath(__file__)), '../src'))
from jobs import insert_monthly_report


def test_insert_db_no_connection():
    df = pd.DataFrame({'A': ['a', 'a'], 'B': ['b', 'b']})
    with pytest.raises(OperationalError):
        insert_monthly_report.insert_db(df, 'table_name')
