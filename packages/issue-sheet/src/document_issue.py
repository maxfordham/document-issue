# -*- coding: utf-8 -*-
"""
Created on Fri Feb  14 13:37:03 2019

@author: o.beckett
"""

import sys
import pathlib
import xlwings as xw
from d_i_ui import warning_messagebox
from d_i_gui import run


from datetime import datetime

gettime = lambda: datetime.now().strftime("%H-%M-%S")
getname = lambda: f"df_{gettime()}.csv"

### The Interface for the number generation###
if __name__ == "__main__":

    print(sys.argv)
    argv = sys.argv[1:]
    fpath = None
    if len(sys.argv) <= 1:
        cmd = run
    elif len(sys.argv) > 1:
        fpth = argv[-1]
        cmd = run

    if __debug__:
        print("Debug ON")
        fpth = pathlib.Path(__file__).parent / "DocumentNumberGenerator.xlsm"
        xw.Book(str(fpth)).set_mock_caller()
        RESULTS = cmd()
    else:
        print("Release Mode")
        try:
            if fpath:
                xw.Book(fpath).set_mock_caller()
            RESULT = cmd()
        except Exception as exc:
            warning_messagebox(message=exc, title="PDF ERROR")
