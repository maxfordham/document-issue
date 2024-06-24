# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 13:37:03 2019

@author: o.beckett
"""

import sys
import pathlib

DIR_ROOT = pathlib.Path(__file__).parent.parent
sys.path.append(str(DIR_ROOT))

from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm
from mf_reportlab.mf_styles import table, DEFAULTTABLESTYLE


###INFO TABLE DATA###
INFODATA = [
    ["Client Name:", "MYCLIENT"],
    ["Project Name:", "MYPROJECTNAME"],
    ["Job Number:", "J0000"],
    ["Project Address:", "MYPROJECTADDRESS"],
]


def issue_sheet(
    data,
    document,
    titleblockdata=[],
    headings=[[""] * 4] * 4,
    tablestyle=DEFAULTTABLESTYLE(),
    col_widths=[100, 40, 9],
):
    """populate and draw the issue sheet"""

    data2 = headings + data
    document.set_page_size(landscape(A3))

    ###CONTENT###
    Elements = []  ###List of everything in order.
    Elements = table(
        data2, Elements, tablestyle=tablestyle, col_widths=[i * mm for i in col_widths]
    )  # Highlight everything that equals Basement can replace with more sophisticated conditions.

    document.go(Elements, titleblockdata)

    return document


# create doc


# max_cols_in_part
# outgoingfolder
# column_widths
# office
# selected_issues
