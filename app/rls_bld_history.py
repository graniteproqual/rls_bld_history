import json
import os
import re
from datetime import datetime
from inspect import currentframe, getframeinfo

"""
Read and write the release build history
This is stub for testing:
as of 7/24/2021, We haven't yet finalized data store mechanism and
for the bld_rls_history, but will use a json object for now to support testing
"""


class Rls_bld_history:

    def __init__(self, rls_bld_history_store_filepath=None):
        default = "./data/rls_bld_history.json"
        if(rls_bld_history_store_filepath is None):
            self.rls_bld_history_store_filepath = default
        else:
            self.rls_bld_history_store_filepath = rls_bld_history_store_filepath  # <<<<-----

        self.quarter_schemes = {
            "normal": {"03": 'Mar',
                       "06": 'Jun',
                       "09": "Sep",
                       "12": "Dec"
                       },
            "jun_dec": {"06": 'Jun',
                        "12": "Dec"
                        },
            "dec": {"12": "Dec"}
        }
        self.product_quarter_schemes = {
            "CRP": "normal",
            "FFPL": "normal",
            "BDR": "dec",
            "FFPS": "jun_dec"
        }


# {
#     "products": {
#         "CRP": {
#             "latest_release": "pending",
#             "years": {
#                 "2020": {
#                     "quarters":
#                         {
#                             "03": {
#                                 "latest_build": "2",
#                                 "builds": {
#
# {'products': {'CRP': {{'latest_release': 'pending'}, {'years': {'2020': {'quarters': 'pending'}}}}}}


    def read_json_file(self, json_filepath):
        retval = None
        with open(json_filepath, "r") as jsonfile:
            retval = json.load(jsonfile)
        return retval

    def read_rls_bld_history(self):
        json_filepath = self.rls_bld_history_store
        self.rls_bld_history = self.read_json_file(json_filepath)
        return(self.rls_bld_history)

    def write_rls_bld_history(self):
        with open(self.rls_bld_history_store, "w") as jsonfile:
            json.dump(self.rls_bld_history, jsonfile, indent=4)

    def start_a_new_product(self, pdt, year=None, qtr=None, tgtrls=None, bld=None):
        self.add_product(pdt)
        self.add_year(pdt, year)
        self.add_quarter(pdt, year, qtr)
        self.add_target_release(pdt, year, qtr, tgtrls)
        self.add_build(pdt, year, qtr, tgtrls, bld)
        assert self.build_exists(pdt, year, qtr, tgtrls, bld)

    def product_exists(self, pdt):
        retval = False
        if(self.rls_bld_history["products"]):
            products = self.rls_bld_history["products"].keys()
            if(products is not None):
                if(pdt in products):
                    retval = True
        return retval

    def add_product(self, pdt):
        product_exists = self.product_exists(pdt)
        if(not product_exists):
            self.rls_bld_history["products"][pdt] = {}
            self.rls_bld_history["products"][pdt].update({"last_maintenance_release": "pending"})
            self.rls_bld_history["products"][pdt].update({"last_mainline_release": "pending"})
            self.rls_bld_history["products"][pdt].update({"years": {}})
            self.write_rls_bld_history()
        return

    def year_exists(self, pdt, year):
        years = self.rls_bld_history["products"][pdt]["years"].keys()
        retval = False
        if(years is not None):
            if(year in years):
                retval = True
        return retval

    def get_years(self, pdt, year):
        years = self.rls_bld_history["products"][pdt]["years"].keys()
        return years

    def latest_year(self, pdt):
        retval = "pending"
        years = list(self.rls_bld_history["products"][pdt]["years"].keys())
        if(years):
            retval = max(years)
        return retval

    def increment_year(self, pdt):
        new_year = str(int(self.latest_year(pdt)) + 1)
        return new_year + 1

    def add_year(self, pdt, year):
        if year:
            if(not self.year_exists(pdt, year)):
                self.rls_bld_history["products"][pdt]["years"][year] = {}
                self.rls_bld_history["products"][pdt]["years"][year].update({"quarters": {}})
                self.write_rls_bld_history()

    def delete_pending_year(self, pdt):
        del self.rls_bld_history["products"][pdt]["years"]["pending"]

    def quarter_exists(self, pdt, year, qtr):
        quarters = self.get_quarters(pdt, year)
        retval = False
        if(quarters is not None):
            if(qtr in quarters):
                retval = True
        return retval

    def get_quarters(self, pdt, year):
        return self.rls_bld_history["products"][pdt]["years"][year]["quarters"].keys()

    def latest_quarter(self, pdt, year):
        pass

    def add_quarter(self, pdt, year, qtr=None):
        scheme = self.product_quarter_schemes[pdt]
        if(qtr is None):
            latest_quarter = self.latest_quarter(pdt, year)
            qtr = self.gen_next_quarter(latest_quarter, scheme)
        if not self.quarter_exists(pdt, year, qtr):
            self.rls_bld_history["products"][pdt]["years"][year]["quarters"][qtr] = {}
            self.rls_bld_history["products"][pdt]["years"][year]["quarters"][qtr].update({"target_release": {}})
        self.write_rls_bld_history()

    def add_target_release(self, pdt, year, qtr, tgtrls=None):
        # todo - try to determine next target release based on previous target release, 
        # and handle if no previous target release for quarter
        # if tgt_rls is None:
            # ...
        if not self.target_release_exists(pdt, year, qtr, tgtrls):
            self.rls_bld_history["products"][pdt]["years"][year]["quarters"][qtr]["target_release"] = {}
            self.rls_bld_history["products"][pdt]["years"][year]["quarters"][qtr]["target_release"].\
                update({tgtrls: {"builds": {}}})
        self.write_rls_bld_history()

    def target_release_exists(self, pdt, year, qtr, tgtrls):
        retval = False
        target_releases = self.get_target_releases(pdt, year, qtr)
        if(target_releases is not None):
            if(tgtrls in target_releases):
                retval = True
        return retval

    def get_target_releases(self, pdt, year, qtr):
        """Get list of all target releases for a product - year - quarter"""
        return self.rls_bld_history["products"][pdt]["years"][year]["quarters"][qtr]["target_release"].keys()

    def get_latest_target_release(self, pdt, year, qtr):
        """Determine last/latest target release for a product, year, quarter"""
        latest_target_release = self.rls_bld_history[pdt][year][qtr]
        return latest_target_release

    def determine_next_target_release(self, pdt, year, qtr):
        """todo"""
        pass

    def latest_quarter(self, product, year):
        """Determine latest quarter for a product - year"""
        quarters = list(self.rls_bld_history["products"][product]["years"][year]["quarters"].keys())
        return(max(quarters))

    def gen_next_quarter(self, latest_quarter, quarter_scheme="normal"):
        """Generate next quarter id based on quarter scheme and latest quarter id recorded in rls_bld_history"""
        """todo"""
        # scheme = self.quarter_schemes[quarter_scheme]
        # keys = list(scheme.keys())
        # last_key_in_scheme = keys[-1]
        # first_key_in_scheme = keys[0]
        # last_quarter_index = keys.index(latest_quarter)
        # if(quarter_scheme == 'normal'):
        #     if(latest_quarter == last_key_in_scheme):
        #         next_quarter = first_key_in_scheme
        #     else:
        #         next_quarter = keys[last_quarter_index + 1]
        # return(next_quarter)

    def add_build(self, pdt, year, qtr, tgtrls, bld=None):
        """Add a build to rls_bld_history"""
        retval = False
        self.add_product(pdt)
        self.add_year(pdt, year)
        self.add_quarter(pdt, year, qtr)
        self.add_target_release(pdt, year, qtr, tgtrls)
        self.rls_bld_history["products"][pdt]["years"][year]["quarters"][qtr]["target_release"][tgtrls]["builds"] = {}
        self.rls_bld_history["products"][pdt]["years"][year]["quarters"][qtr]["target_release"][tgtrls]["builds"].\
            update({bld: {"DateTime": self.iso_datetime_now_string()}})
        self.write_rls_bld_history()
        if(self.build_exists(pdt, year, qtr, tgtrls, bld)):
            retval = True
        return retval

    def build_exists(self, pdt, year, qtr, tgtrls, bld):
        """Check if a build exists in rls_bld_history"""
        builds = self.get_builds(pdt, year, qtr, tgtrls)
        retval = False
        if(builds is not None):
            if(bld in builds):
                retval = True
        return retval

    def get_builds(self, pdt, year, qtr, tgtrls):
        """Get all build numbers for a product - year - quarter - target release"""
        return self.rls_bld_history["products"][pdt]["years"][year]["quarters"][qtr]["target_release"][tgtrls]["builds"].keys()

    def parse_release_or_build(self, rls_bld_string):
        """ Release:
        "Product_MmmYY.Tgtrls"
        e.g.
        "CRP_Mar20.0"  -> mainline release for CRP for March Quarter of 2020
        "CRP_Mar20.3"  -> 3rd maintenance release for CRP for March Quarter of 2020

        "Product_MmmYY.Tgtrls.Build"
        e.g.
        "CRP_Mar20.0.13  -> 13th build for mainline release for CRP for March Quarter of 2020
        "CRP_Mar20.2.7   -> 7th build for 2nd maintenance release for CRP for March Quarter of 2020
        """
        r = r"^([a-zA-Z0-9]+)_(MAR|JUN|SEP|DEC)([2|3|4][0-9])\.([0-9]+)$"
        re_for_release = re.compile(r, re.IGNORECASE)
        b = r"^([a-zA-Z0-9]+)_(MAR|JUN|SEP|DEC)([2|3|4][0-9])\.([0-9]+)\.([0-9]+)$"
        re_for_build = re.compile(b, re.IGNORECASE)

        retval = None
        match = re.search(re_for_release, rls_bld_string)
        if match:
            retval = {
                "product": match.group(1),
                "quarter": match.group(2),
                "year": match.group(3),
                "target_release": match.group(4)
            }
        else:
            match = re.search(re_for_build, rls_bld_string)
            if match:
                retval = {
                    "product": match.group(1),
                    "quarter": match.group(2),
                    "year": match.group(3),
                    "target_release": match.group(4),
                    "build": match.group(5)
                }
        return retval

    def latest_release(self, pdt):
        # rls_bld_history = self.set_up_rls_bld_history_if_needed(prd)
        # retval = self.rls_bld_history["products"][product]["latest_release"]
        # return(retval)
        pass

    def add_new_release(self, pdt, year, qtr):
        pass

    """initialize a new rls_bld_history store"""

    def init_a_rls_bld_history_store(self, pytestconfig=None, filepath=None):
        if(filepath is None):
            filepath = "./data/" + self.iso_datetime_now_string() + ".json"
        basename_part = os.path.basename(filepath)
        path_part = os.path.normpath(os.path.dirname(filepath))
        os.makedirs(path_part, exist_ok=True)
        full_name = os.path.join(path_part, basename_part)
        self.rls_bld_history_store = full_name
        self.rls_bld_history = {"products": {}}
        self.write_rls_bld_history()
        return(full_name)

    def iso_datetime_now_string(self):
        return(datetime.now().isoformat(timespec="seconds"))

    def show_history(self):
        print("================================================")
        print(self.rls_bld_history)
        print("=================================================")

    """
    How to do a build for a product:
    1) For product, determine latest year
    2) determine latest quarter for latest year
    3) if there is no mainline release then build has to be for mainline
    4) if there is a mainline release then build has to maintenance
    """

    # def add_build(self, pdt, year=None, qtr=None):
    #     if year is None:
    #         year = self.get_latest_year(pdt, year)  # try to get from history

    #     qtr = self.getquarter(pdt, year, qtr)
    #     if(qtr is None):
    #         qtr = self.latest_quarter(pdt, year, qtr)
    #         if(qtr is None):
    #             # get a likely quarter
    #             qtr = self.get_best_guess_for_quarter(pdt)

    def getyear(self, pdt, year):
        if(year is None):
            year = self.latestyear(pdt)
        if(year is None):
            year = datetime.now().strftime("%Y")
        return year

    def getquarter(self, pdt, year, qtr):
        if(qtr is None):
            qtr = self.latest_quarter(pdt, year, qtr)
            if(qtr is None):
                # get a likely quarter
                qtr = self.get_best_guess_for_quarter(pdt)
        return qtr

    def get_best_guess_for_quarter(pdt):
        # todo figure out how to do this later,
        # for now just select a quarter based on simple selection
        # current quarter_schemes:
        # "normal":      "03"  "06"  "09"  "12"          e.g. CRP, FFPL
        # "jun_dec":           "06"        "12"          e.g. FFPS
        # "dec":                           "12"          e.g. BDR
        # so a good guess would be that the "current" quarter ...
        # we are working on extends...
        # from 16 days after the end of the previous filing month
        # to   15 days after the end of the next     filing month
        # e.g for "normal", 2nd quarter,
        # from 04/16/2020 to 07/15/2020
        # e.g. for "dec"
        # from 01/16/2020 to 01/15/2021
        #
        # figure out a table to facilitate selecting quarter
        pass


if __name__ == "__main__":
    pass
    # store = init_a_rls_bld_history_store(filepath=None)

    # rbh = Rls_bld_history(store)

    # print(rbh.rls_bld_history_store)

    # rbh.rls_bld_history_store = "./data/rls_bld_history.json"
    # filename with datetime stamp
    # OrangeHRM.rslt.2021-04-18T174508.html
    # return(dt.strftime("%d/%m/%Y %H:%M:%S"))
    # fname = rbh.iso_datetime_now_string() + ".json"
    # print(fname)
    # rls_qtr_history.
    # rbh.init_a_rls_bld_history_store(fname)

    # prd = "CRP"
    # latest_release = "pending"
    # # latest_release = rbh.latest_release(prd)
    # print("latest_release is " + latest_release)
    # rls_bld_history = rbh.read_rls_bld_history()
    # print(rls_bld_history)

    # p = "CRP"
    # y = "2020"
    # q = "03"
    # b = "2"
    # s = rls_bld_history["products"][p]["years"][y]["quarters"][q]["builds"][b]
    # print(s)

    # print(rbh.latest_release("CRP"))
    # print(rbh.latest_quarter("CRP", "2020"))
    # """
    # g = input("enter path/filename to new rls_bld_history_store file: ")
    # # storename = init_a_rls_bld_history_store(g)
    # storename = rbh.init_a_rls_bld_history_store(g)
    # print(storename)
    # """
    # print(rbh.latest_quarter("CRP", "2020"))
    # next_quarter = rbh.gen_next_quarter(rbh.latest_quarter("CRP", "2020"), quarter_scheme="normal")
    # print(next_quarter)

    # # filename with datetime stamp
    # # OrangeHRM.rslt.2021-04-18T174508.html
    # # return(dt.strftime("%d/%m/%Y %H:%M:%S"))
    # fname = rbh.iso_datetime_now_string() + ".json"
    # print(fname)
    # # rls_qtr_history.
    # # rbh.init_a_rls_bld_history_store()
    # prd = "CRP"
    # # latest_release = rbh.latest_release(prd)
    # # print("latest_release is " + latest_release)

    # # storename = rbh.init_a_rls_bld_history_store("./data/rls_bld_history.json")
    # rbh.read_rls_bld_history()
    # pdt = "CRP"
    # rbh.product_exists(pdt)
    # pdt = "FFPL"
    # if(not rbh.product_exists(pdt)):
    #     rbh.add_product(pdt)
    #     print("product: " + pdt)
    #     rbh.show_history()
    #     print("================================================")
    #     print(rbh.rls_bld_history)
    #     print("=================================================")

    # year = "2020"
    # if(not rbh.year_exists(pdt, year)):
    #     rbh.add_year(pdt, year)
    #     rbh.year_exists(pdt, year)
    #     print("year : " + year)
    #     rbh.show_history()
    # rbh.write_rls_bld_history()

    # pdt = "BDR"
    # qtr = "12"
    # if(not rbh.product_exists(pdt)):
    #     rbh.add_product(pdt)
    #     print("product: " + pdt)
    #     rbh.show_history()

    # # year = "2020"
    # # if(not rbh.year_exists(pdt, year)):
    # #     rbh.add_year(pdt, year)
    # #     rbh.year_exists(pdt, year)
    # #     print("year : " + year)
    # #     rbh.show_history()
    # #     rbh.write_rls_bld_history()
    # year = rbh.latest_year(pdt)
    # lctr = getframeinfo(currentframe()).lineno
    # if(year == 'pending'):
    #     year = datetime.now().strftime("%Y")
    #     rbh.delete_pending_year(pdt)
    #     rbh.add_year(pdt, year)
    # rbh.write_rls_bld_history()

    # rbh.add_quarter(pdt, year, qtr)

    # pdt = 'FFPL'
    # qtr = "03"
    # year = "2020"
    # if(not rbh.quarter_exists(pdt, year, qtr)):
    #     rbh.add_quarter(pdt, year, qtr)
    #     rbh.quarter_exists(pdt, year, qtr)
    #     rbh.show_history()
    #     rbh.write_rls_bld_history()

    # # year = "2020"
    # # if(not rbh.quarter_exists(pdt, year, qtr)):
    # rbh.add_quarter(pdt, year, "12")
    # #rbh.quarter_exists(pdt, year, qtr)
    # rbh.show_history()
    # rbh.write_rls_bld_history()

    # #rbh.add_build( pdt, year=None, qtr = None, bld = None)
    # # print(type(j))
    # # print(j)
    # # # j["products"][prd]["years"]['2020']['quarters']['09']['latest_build'] = '1'
    # # (j["products"][prd]["years"]['2020']['quarters']).update(
    # #     {'09': {'latest_build': '1', 'builds': {"1": {"datetime": '2020-06-18 10:30:21'}}}})
    # # print("===========================================================")
    # # print(j)
    # # rbh.write_rls_bld_history()
    # rbh = Rls_bld_history()
    # store = rbh.init_a_rls_bld_history_store()
    # print(store)
    # rbh.set_up_rls_bld_history_if_needed("CRP")
