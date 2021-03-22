# coding: utf-8

# Generic libs.
import pytest
import sys
from os.path import join, dirname, realpath

# Project modules to test.
sys.path.insert(0, join(dirname(realpath(__file__)), '../src'))
from utils import fs


def test_list_files():
    assert isinstance(fs.list_files('.'), list)

def test_list_files_integer_path():
    with pytest.raises(ValueError):
        fs.list_files(123)

def test_list_files_non_existing_path():
    return_list = fs.list_files('this/path/do/not/exist')
    assert isinstance(return_list, list)
    assert len(return_list) == 0
