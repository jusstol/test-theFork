# coding: utf-8

# Generic libs.
import os
import logging

# Third party libs.
import pandas as pd

# Project modules.
from utils.fs import mv_file

# Logger.
logger = logging.getLogger(__name__)


def read_csv(file):
    df = pd.read_csv(file, parse_dates=['date'])
    return df

def write_csv(df, data_out_processed, filename_out):
    os.makedirs(data_out_processed, exist_ok=True)
    output_file = os.path.join(data_out_processed, filename_out)
    df.to_csv(output_file, index=False)

def run(file, conf):

    # Parse configuration.
    data_out = conf['data_out']
    data_out_processed = conf['data_out_processed']
    filename_out = conf['filename_out']

    # Read input file.
    try:
        df = read_csv(file)
    except FileNotFoundError as e:
        logger.warning(f"Could not load {file} ({e})")
        return

    # Save currency in a separate column and make 'amount' more usable.
    df['amount'] = df.amount.str.replace(r'[^\.,0-9]', '', regex=True) \
        .str.replace(',', '.').astype(float)

    # Create a month column as 'YYYY_MM'.
    df['month'] = df.date.dt.strftime("%Y_%m")

    # Compute monthly metrics.
    df = df.groupby(['restaurant_id', 'restaurant_name', 'country', 'month']) \
        .agg(number_of_bookings=('booking_id', 'count'),
             number_of_guests=('guests', 'sum'),
             amount=('amount', 'sum')) \
        .reset_index()
    df['amount'] = df.amount.round(2)
    df = df.sort_values(['restaurant_name', 'month'])

    # Write output as CSV file.
    try:
        write_csv(df, data_out_processed, filename_out)
    except OSError as e:
        logger.error(f"Could not write output file {output_file} ({e})")
        return

    # Move input file to output location.
    try:
        mv_file(file, dest=data_out)
    except OSError as e:
        logger.error(f"Could not move {file} to {data_out} ({e})")
        return
