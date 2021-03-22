# coding: utf-8

# Generic libs.
import logging

# Third party libs.
import pandas as pd
from sqlalchemy.exc import OperationalError

# Project modules.
from sql import db
from utils.fs import mv_file

# Logger.
logger = logging.getLogger(__name__)


def insert_db(df, table_out):
    engine = db.connect()
    logger.info(f"Inserting into {table_out} table")
    df.to_sql(name=table_out, con=engine, if_exists='append', index=False)

def run(file, conf):

    # Parse configuration.
    data_out = conf['data_out']
    table_out = conf['table_out']

    # Read source file.
    logger.info(f"Processing {file}")
    try:
        df = pd.read_csv(file)
    except FileNotFoundError as e:
        logger.warning(f"Could not load {file} ({e})")
        return

    # Insert into database.
    try:
        insert_db(df, table_out=table_out)
    except OperationalError as e:
        logger.error(f"Problem while trying to insert to database ({e})")
        return

    # Move input file to output location.
    try:
        mv_file(file, dest=data_out)
    except OSError as e:
        logger.error(f"Could not move {file} to {data_out} ({e})")
