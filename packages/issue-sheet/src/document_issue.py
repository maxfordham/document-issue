# -*- coding: utf-8 -*-
"""
Created on Fri Feb  14 13:37:03 2019

@author: o.beckett
"""

import sys, getopt
import pathlib
import xlwings as xw
import pandas as pd
import math as math
from reportlab.lib import colors
from d_i_ui import warning_messagebox, info_messagebox, getsavefilename, getfoldername
from d_i_ui import MFButton, MFLabelFrame, MFLabel, MFLabelBlack
from d_i_ui import MFHeader, MFOptionMenu, MFCheckButton, MFTk
from mf_reportlab.issuesheet_reportlab import issue_sheet
from mf_reportlab.mf_styles import MFDoc, DEFAULTTABLESTYLE, highlight_last_format
from mf_reportlab.mf_styles import p_nospace, get_titleblockimage
from mf_reportlab.mf_styles import dist_line_style, sid_line_style, small_grey_style
from constants import address_from_loc, address_from_loc_compact, OFFICES
from d_i_ui import warning_messagebox
from d_i_gui import DialogWindow, NumGeneratorWindow, run

from datetime import datetime
gettime = lambda: datetime.now().strftime('%H-%M-%S')
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
        print('Debug ON')
        fpth = pathlib.Path(__file__).parent / 'DocumentNumberGenerator.xlsm'
        xw.Book(str(fpth)).set_mock_caller()
        RESULTS = cmd()
    else:
        print('Release Mode')
        try:
            if fpath:
                xw.Book(fpath).set_mock_caller()
            RESULT = cmd()
        except Exception as exc:
            warning_messagebox(message=exc, title="PDF ERROR")
