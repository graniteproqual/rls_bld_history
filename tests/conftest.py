import json
import os
import sys
import unittest
from datetime import datetime

import pytest
from rls_bld_history import Rls_bld_history


# @pytest.fixture
def test_config():
    return {
        "compare_data_folder": "tests/compare_data/"
    }


def pytest_addoption(parser):
    parser.addoption("--datetimestring", action="store", default=None)


# @pytest.fixture
def json_are_equivalent(json1, json2):
    return(json.dumps(json1, sort_keys=True) == json.dumps(json2, sort_keys=True))

#     return request.config.getoption("--datetimestring")


# @pytest.fixture
# def rls_bld_history_filename(pytestconfig):
#     filename = pytestconfig.getoption("datetimestring")
#     """ create a filename based on date and time created e.g. 2021-08-08T11:58:29.json """
#     # return("./data/" + (datetime.now().isoformat(timespec="seconds")) + ".json")
#     return("./data/" + filename + ".json")


# @classmethod
# def setup_class(Test_rls_bld_history):
#     Test_rls_bld_history.filepath = "./data/" + (datetime.now().isoformat(timespec="seconds")) + ".json"
#     print("---------------------------------------------------------------------------------------")
#     print("-----------in setup_class : " + Test_rls_bld_history.filepath + "----------------------")
#     print("---------------------------------------------------------------------------------------")
#     # Test_rls_bld_history.rls_bld_history_filepath = filepath
#     Test_rls_bld_history.rbh = \
#         Rls_bld_history(Test_rls_bld_history.filepath)
