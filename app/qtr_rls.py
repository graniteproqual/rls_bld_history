#!/Users/jc/projects/python_projects/qtr_rls/.venv/bin/python3
from datetime import datetime

#from rls_bld_history import Rls_bld_history as rls_bld_history

#from typing_extensions import ParamSpecArgs


"""
qtr_rls.py
Functionality to support creating, and working with, release/Build identifiers with PRODUCT_MMMYY.RLS.BLD format
where PRODUCT corresponds to the Product that is released on a "quarterly" schedule
and MMM corresponds to a quarter month ("MAR", "JUN", "SEP", "DEC")
and YY corresponds to a two digit year, "00 for 2000, through "99" for 2099
and RLS is the release incrementor
    (starting at zero for first release of the quarter)
    (and incrementing by 1 for every subsequent "fix" release of the quarter)
and BLD corresponds to the build working toward the release
"""

QUARTERS = ["Mar", "Jun", "Sep", "Dec"]
QUARTER_NUMBERS = [3, 6, 9, 12]
QUARTERS_DICT = {QUARTER_NUMBERS[i]: QUARTERS[i] for i in range(len(QUARTER_NUMBERS))}
QUARTER_NUMBERS_DICT = {QUARTERS[i]: QUARTER_NUMBERS[i] for i in range(len(QUARTER_NUMBERS))}


def datestamp(dt=datetime.now()):
    """string format of date to save with builds and releases"""
    return(dt.strftime("%d/%m/%Y %H:%M:%S"))


def read_rls_bld_history():
    pass


if __name__ == "__main__":
    d = datestamp()
    print(d)
    print(QUARTERS_DICT)
    print(QUARTER_NUMBERS_DICT)
