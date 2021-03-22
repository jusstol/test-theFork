# coding: utf-8

# Generic librairies.
import os

# Local directories.
DIR_DATA_IN = os.getenv('DIR_DATA_IN')
DIR_DATA_PROCESS = os.getenv('DIR_DATA_PROCESS')
DIR_DATA_OUT = os.getenv('DIR_DATA_OUT')

# Database details.
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', 5432))
