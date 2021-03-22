# coding: utf-8

# Third party libs.
import sqlalchemy

# Project modules.
from conf.env import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, \
    POSTGRES_HOST, POSTGRES_PORT


def connect():
    """Returns engine object to connect to Postgres database."""
    connection_str = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    engine = sqlalchemy.create_engine(connection_str, connect_args={'connect_timeout': 1})
    return engine
