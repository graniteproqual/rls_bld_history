import inspect
import os
from datetime import datetime

import pytest
from rls_bld_history import Rls_bld_history

import conftest as ct  # to run tests from this file

UL_BOLD_RED = '\033[4m' + '\033[1m' + '\033[91m'


def passmsg(currtest, msg=""):
    if(len(msg) > 0):
        msg = " : " + msg
    print("\n * " + currtest + msg, end="")


class Test_rls_bld_history():
    @pytest.fixture(autouse=True, scope='class')
    def setup_class(self):
        filepath = "./data/" + (datetime.now().isoformat(timespec="seconds")) + ".json"
        Test_rls_bld_history.rbh = Rls_bld_history(filepath)
        # Test_rls_bld_history.rls_bld_history_filepath = filepath

    # def __init__(self):
    #     rls_bld_history_filepath = "./data/" + (datetime.now().isoformat(timespec="seconds")) + ".json"
    #     self.rbh = Rls_bld_history(rls_bld_history_filepath)
    #     self.rbh.rls_bld_histor

    # def init_a_rls_bld_history_store(self, filepath):
    #     """
    #     just create an empty store to eventually contain the rsl_bld_history
    #     store will be named based on time created e.g. 2021-08-08T11:58:29.json
    #     store will be used for tests i this test class
    #     """
    #     print("******* in init_a_rls_bld_history_store with filepath = " + filepath)
    #     basename_part = os.path.basename(filepath)
    #     path_part = os.path.normpath(os.path.dirname(filepath))
    #     os.makedirs(path_part, exist_ok=True)
    #     full_name = os.path.join(path_part, basename_part)
    #     f = open(full_name, 'w')  # "w" flag will empty file if it exists
    #     f.close()
    #     return

    @pytest.mark.first_two
    @pytest.mark.test_to_initial_rls_bld_history_json_compare
    def test_existence_of_Rls_bld_history_instance(self):
        curr_test = inspect.currentframe().f_code.co_name
        assert self.rbh, curr_test + " failed"
        passmsg(curr_test, " passed, rbh object is created")

    @pytest.mark.first_two
    @pytest.mark.test_to_initial_rls_bld_history_json_compare
    def test_create_Release_Build_History_Store(self):
        self.rbh.init_a_rls_bld_history_store()
        store_exists = os.path.isfile(self.rbh.rls_bld_history_store_filepath)
        curr_test = inspect.currentframe().f_code.co_name
        assert store_exists, curr_test + " failed, history file is " + self.rbh.rls_bld_history_store_filepath
        passmsg(curr_test, " passed, history file is " + self.rbh.rls_bld_history_store_filepath)

    # @pytest.mark.depends(on=["test_create_Release_Build_History_Store"])
    @pytest.mark.test_to_initial_rls_bld_history_json_compare
    def test_add_product_CRP_to_rls_bld_history(self):
        pdt = "CRP"
        self.rbh.add_product(pdt)
        curr_test = inspect.currentframe().f_code.co_name
        assert self.rbh.product_exists(pdt), curr_test + " FAILED: product: " + pdt + " was not added"
        passmsg(curr_test, " passed: product: " + pdt + " was added")

    @pytest.mark.test_to_initial_rls_bld_history_json_compare
    def test_add_year_to_product_CRP(self):
        year = "2020"
        pdt = "CRP"
        self.rbh.add_year(pdt, year)
        self.rbh.write_rls_bld_history()
        curr_test = inspect.currentframe().f_code.co_name
        assert self.rbh.year_exists(pdt, year), curr_test + " FAILED: year: " + year + " was not added to " + pdt
        passmsg(curr_test, " passed: product: " + year + " was added to " + pdt)

    @pytest.mark.test_to_initial_rls_bld_history_json_compare
    def test_add_quarter_03_to_product_CRP_and_year_2020(self):
        year = "2020"
        pdt = "CRP"
        qtr = "03"
        self.rbh.add_quarter(pdt, year, qtr)
        self.rbh.write_rls_bld_history()
        curr_test = inspect.currentframe().f_code.co_name
        assert self.rbh.quarter_exists(pdt, year, qtr), curr_test + " FAILED: quarter: " + qtr + \
            " was not added for year: " + year + " and product: " + pdt
        passmsg(curr_test, " passed: quarter: " + qtr + " was added for product: " + pdt +
                " and year: " + year)

    @pytest.mark.test_to_initial_rls_bld_history_json_compare
    def test_initial_CRP_excerpt_matches_baseline_initial_CRP_excerpt(self):
        initial_crp_excerpt = self.rbh.read_rls_bld_history()
        baseline_initial_CRP_excerpt = \
            self.rbh.read_json_file(
                ct.test_config()["compare_data_folder"] +
                "CRP_year-2020-Quarter-03_no-release_no_builds.json")

        equivalent = (ct.json_are_equivalent(initial_crp_excerpt, baseline_initial_CRP_excerpt))
        curr_test = inspect.currentframe().f_code.co_name
        assert equivalent, curr_test + " FAILED"
        passmsg(curr_test, " passed")

    def test_add_build_for_CRP_20_03(self):
        pdt = "CRP"
        year = "2020"
        qtr = "03"
        tgtrls = "2"
        bld = "3"
        self.rbh.add_build(pdt, year, qtr, tgtrls, bld)
        curr_test = inspect.currentframe().f_code.co_name

        assert self.rbh.build_exists(pdt, year, qtr, tgtrls, bld), curr_test + \
            " FAILED: build: " + bld + " was not added to " + pdt
        passmsg(curr_test, " passed: build: " + bld + " was added to " + pdt)

    def test_start_a_new_product(self):
        pdt = "FFPL"
        year = "20"
        qtr = "06"
        tgtrls = "0"
        bld = "1"
        ffpl = self.rbh.start_a_new_product(pdt, year, qtr, tgtrls, bld)
        curr_test = inspect.currentframe().f_code.co_name
        assert self.rbh.build_exists(pdt, year, qtr, tgtrls, bld), "New product FFPL and all elements to build was not created"
        passmsg(curr_test, "New product FFPL and all elements to build = {}: was  created".format(bld))

    @pytest.mark.parse_release_and_build
    def test_parsing_a_good_mainline_release_id(self):
        release_id = "CRP_Mar20.0"
        dict = self.rbh.parse_release_or_build(release_id)
        curr_test = inspect.currentframe().f_code.co_name
        assert(
            (dict["product"] == "CRP") and
            (dict["quarter"] == 'Mar') and
            (dict["year"] == "20") and
            (dict["target_release"] == "0")
        ), " FAILED " + dict["product"] + "_" + dict["quarter"] + dict["year"] + "." + dict["target_release"]
        passmsg(curr_test, " passed " + dict["product"] + "_" + dict["quarter"] + dict["year"] + "." + dict["target_release"])

    @pytest.mark.parse_release_and_build
    def test_parsing_a_good_mainline_build_id(self):
        release_id = "CRP_Mar20.0.17"
        dict = self.rbh.parse_release_or_build(release_id)
        curr_test = inspect.currentframe().f_code.co_name
        assert(
            (dict["product"] == "CRP") and
            (dict["quarter"] == 'Mar') and
            (dict["year"] == "20") and
            (dict["target_release"] == "0") and
            (dict["build"] == "17")
        ), " FAILED " + dict["product"] + "_" + dict["quarter"] + dict["year"] + "." + dict["target_release"] + dict["build"]

        passmsg(
            curr_test,
            " passed " +
            dict["product"] +
            "_" +
            dict["quarter"] +
            dict["year"] +
            "." +
            dict["target_release"] +
            "." +
            dict["build"])

    @pytest.mark.parse_release_and_build
    def test_parsing_a_BAD_mainline_build_id(self):
        release_id = "AAAAAAAAAA"
        dict = self.rbh.parse_release_or_build(release_id)
        curr_test = inspect.currentframe().f_code.co_name

        assert(dict is None)
        passmsg(curr_test, "parse_release_or_build('AAAAAAAA') returned False indicating a 'BAD' build id")

    @pytest.mark.skip(reason="test not ready: test_add_a_quarter_that_already_exists")
    def test_add_a_quarter_that_already_exists(self):
        assert False, UL_BOLD_RED + "Still need todo" + '\033[0m'

    @pytest.mark.skip(reason="test not ready: test_gen_a_release_id")
    def test_gen_a_release_id(self):
        pdt = "CRP"
        year = "20"
        qtr = "03"
        bld = "4"
        assert False, UL_BOLD_RED + "Still need todo" + '\033[0m'


if(__name__ == "__main__"):
    t = Test_rls_bld_history()
    t.test_create_Release_Build_History_Store()
