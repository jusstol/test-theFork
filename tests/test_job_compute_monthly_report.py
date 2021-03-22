# coding: utf-8

# Generic libs.
import pandas as pd
import pytest
import sys
from os.path import join, dirname, realpath

# Project modules to test.
sys.path.insert(0, join(dirname(realpath(__file__)), '../src'))
from jobs import compute_monthly_report


def test_read_non_existing_csv():
    with pytest.raises(FileNotFoundError):
        compute_monthly_report.read_csv('this/file/does/not/exist.csv')


def test_write_csv_empty_dataframe():
    df = pd.DataFrame()
    compute_monthly_report.write_csv(df, join(dirname(realpath(__file__))), 'output.csv')
