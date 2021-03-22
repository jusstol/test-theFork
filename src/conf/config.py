# coding: utf-8

# Generic libs.
import os

# Project modules.
from conf.env import DIR_DATA_IN, DIR_DATA_PROCESS, DIR_DATA_OUT

jobs = {
    'compute_monthly_report': {
        'data_in': DIR_DATA_IN,
        'data_out': os.path.join(DIR_DATA_OUT, 'bookings'),
        'data_out_processed': os.path.join(DIR_DATA_PROCESS, 'monthly_report'),
        'filename_in': r"^bookings\.csv$",
        'filename_out': "monthly_restaurants_report.csv",
        'freq': 1
    },
    'insert_monthly_report': {
        'data_in': os.path.join(DIR_DATA_PROCESS, 'monthly_report'),
        'data_out': os.path.join(DIR_DATA_OUT, 'monthly_report'),
        'filename_in': r"^monthly_restaurants_report\.csv$",
        'table_out': "monthly_restaurants_report",
        'freq': 1
    },  # easy to add jobs configurations
}
