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
        # fpth = (
        #     pathlib.Path(__file__).parent.parent.parent
        #     / "xl"
        #     / "DocumentNumberGenerator-v0_0_12.xlsm"
        # )
        # fpth = pathlib.Path(
        #     r"J:\J7004\Issue Sheet\Stage 4 - Construction\J7004_DocumentNumberGenerator_Construction.xlsm"
        # )
        # fpth = pathlib.Path(
        #     r"J:\J7081\Project Management\Job Running\J7081 Document Number Generator.xlsm"
        # )
        # fpth = (
        #     pathlib.Path(__file__).parent.parent.parent
        #     / "xl"
        #     / "DocumentNumberGenerator-v0_0_7.xlsm"
        # )
        fpth = (
            pathlib.Path(__file__).parent.parent.parent
            / "xl"
            / "DocumentNumberGenerator.xlsm"
        )
        fpth = pathlib.Path(
            r"J:\J6246\Issue Sheets\6246 _Issue Sheet Document Numbers Register.xlsm"
        )
        fpth = pathlib.Path(
            r"J:\J7561\Project Management\Job Running\J7561_DocumentNumberGenerator.xlsm"
        )
        fpth = pathlib.Path(
            r"J:\J6962\Project Management\Job Running\Issue Sheets\MEP\J6962 DocumentNumberGenerator1.xlsm"
        )

        xw.Book(str(fpth)).set_mock_caller()
        RESULTS = cmd()
    else:
        print("Release Mode")
        try:
            if fpath is not None:
                xw.Book(fpath).set_mock_caller()
            RESULT = cmd()
        except Exception as exc:
            warning_messagebox(message=exc, title="PDF ERROR")
