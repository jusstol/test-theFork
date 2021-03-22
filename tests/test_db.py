# coding: utf-8

# Generic libs.
import sqlalchemy
import sys
from os.path import join, dirname, realpath

# Project modules to test.
sys.path.insert(0, join(dirname(realpath(__file__)), '../src'))
from sql import db


def test_connect():
    assert isinstance(db.connect(), sqlalchemy.engine.base.Engine)
