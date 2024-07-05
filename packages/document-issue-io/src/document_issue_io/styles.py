# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 14:14:44 2019
@author: o.beckett
"""
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


###Styles###
STYLES = getSampleStyleSheet()
PARASTYLE = STYLES["Normal"]
HIGHLIGHT_COLOUR = colors.Color(255 / 255, 255 / 255, 255 / 255, alpha=1.0)
CURRENT_COLOUR = colors.Color(205 / 255, 205 / 255, 205 / 255, alpha=1.0)
NUM_HEADER_ROWS = 5
THICKLINE = 2

from .constants import FONTS


def register_fonts():
    for k, v in FONTS.items():  # TODO: use carlito instead of calibri
        fpth = str(v)
        pdfmetrics.registerFont(TTFont(k, fpth))


# (COL, ROW)
def DEFAULTTABLESTYLE(defaultcols=4):
    # defaultcols in the number of columns BEFORE "Rev"
    _style = [
        ("LINEBELOW", (0, 6), (-1, -1), 0.1, colors.grey),  # aplies to all data
        (
            "LINEAFTER",
            (defaultcols + 1, 6),
            (-2, -1),
            0.1,
            colors.grey,
        ),  # applies to all revision data
        (
            "LINEBELOW",
            (defaultcols, 0),
            (-1, 3),
            0.1,
            colors.grey,
        ),  # aplies to Datestatus
        (
            "LINEAFTER",
            (defaultcols + 1, 0),
            (-2, 3),
            0.1,
            colors.grey,
        ),  # applies to Datestatus
        ("LINEABOVE", (0, 0), (-1, 0), THICKLINE, colors.black),  # topline
        ("LINEBELOW", (0, 2), (-1, 2), THICKLINE, colors.black),  # line below date
        (
            "LINEABOVE",
            (0, 4),
            (-1, 4),
            THICKLINE,
            colors.black,
        ),  # line above Document Title
        (
            "LINEBELOW",
            (0, 4),
            (-1, 4),
            THICKLINE,
            colors.black,
        ),  # line below document title
        ("BACKGROUND", (0, 0), (-1, 3), colors.transparent),  # dday-status background
        (
            "TEXTCOLOR",
            (0, 0),
            (2, 3),
            colors.black,
        ),  # everything should be black now...
        ("BACKGROUND", (3, 0), (-1, -1), colors.white),  # ignore the alternating
        ("BACKGROUND", (0, 4), (-1, -1), colors.white),  # ignore the alternating
        ("SPAN", (defaultcols + 1, 4), (-1, 4)),  # dated issue revisions
        ("ALIGN", (defaultcols, 4), (-1, 4), "CENTER"),  # dated issue revisions
        ("FONTNAME", (0, 5), (-1, -1), "Calibri"),  # This should be everything
        ("FONT", (0, 0), (-1, 3), "Calibri", 10),  # day,month,year,status
        ("FONT", (0, 4), (-1, 4), "Calibri-Bold", 16),  # Document Title etc.
        ("FONT", (2, 4), (defaultcols, 4), "Calibri-Bold", 10),  # Size scale
        ("FONT", (0, 5), (-1, -1), "Calibri", 8),  # everything else
        ("TEXTCOLOR", (3, 0), (-1, 4), colors.black),  # needed?
        ("TEXTCOLOR", (0, 4), (-1, 4), colors.black),  # needed?
        (
            "ROWBACKGROUNDS",
            (0, 5),
            (-1, -1),
            [colors.Color(249 / 255.0, 249 / 255.0, 249 / 255.0), colors.white],
        ),  # alternate the colours
        (
            "LINEBEFORE",
            (defaultcols, 4),
            (defaultcols, -1),
            THICKLINE,
            colors.black,
        ),  # revision sides.
        (
            "LINEAFTER",
            (defaultcols, 0),
            (defaultcols, -1),
            THICKLINE,
            colors.black,
        ),  # revision sides
        (
            "ALIGN",
            (defaultcols, 0),
            (defaultcols, 3),
            "RIGHT",
        ),  # Document number column
        ("ALIGN", (1, 3), (1, -1), "RIGHT"),  # day,mnnth year, Rev
        ("ALIGN", (defaultcols, 4), (-2, -1), "CENTER"),
    ]  # applies to all revision data
    return _style
