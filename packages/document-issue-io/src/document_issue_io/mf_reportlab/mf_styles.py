# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 14:14:44 2019
@author: o.beckett
"""
import os
import pathlib
import logging
from contextlib import contextmanager

from reportlab.lib import colors
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    Table,
    Spacer,
    SimpleDocTemplate,
    TableStyle,
    Paragraph,
    Preformatted,
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from document_issue.document_issue import DocumentIssue
from ..title_block import title_block_table

DIR = pathlib.Path(__file__).parent

###Styles###
STYLES = getSampleStyleSheet()
WRAPSTYLE = STYLES["BodyText"]  # TODO implement.
PARASTYLE = STYLES["Normal"]
HEADERSTYLE = STYLES["Heading1"]
HEADERSTYLE2 = ParagraphStyle(
    name="Heading21",
    parent=PARASTYLE,
    fontName="Calibri-Bold",
    fontSize=18,
    leading=22,
    spaceAfter=6,
    underlineWidth=3,
    underlineOffset=-5,
)
ADDRESSSTYLE = STYLES["Normal"]
ADDRESSSTYLE.alignment = TA_RIGHT
LOGO = DIR / "mf_medium.jpg"

NUM_HEADER_ROWS = 5

THICKLINE = 2
HIGHLIGHT_COLOUR = colors.Color(255 / 255, 255 / 255, 255 / 255, alpha=1.0)
CURRENT_COLOUR = colors.Color(205 / 255, 205 / 255, 205 / 255, alpha=1.0)

###FONTS###
###Register Callibri fonts###
TTFFILE = str(DIR / "fonts" / "calibri.ttf")
pdfmetrics.registerFont(TTFont("Calibri", TTFFILE))
TTFFILE = str(DIR / "fonts" / "calibrib.ttf")  # Bold
pdfmetrics.registerFont(TTFont("Calibri-Bold", TTFFILE))
TTFFILE = str(DIR / "fonts" / "calibrili.ttf")  # Light Italics
pdfmetrics.registerFont(TTFont("Calibri-Light-Italics", TTFFILE))
TTFFILE = str(DIR / "fonts" / "calibrii.ttf")  # Italics
pdfmetrics.registerFont(TTFont("Calibri-Italics", TTFFILE))
TTFFILE = str(DIR / "fonts" / "calibril.ttf")  # Light
pdfmetrics.registerFont(TTFont("Calibri-Light", TTFFILE))
TTFFILE = str(DIR / "fonts" / "calibrib.ttf")  # Bold Italics
pdfmetrics.registerFont(TTFont("Calibri-Bold-Italics", TTFFILE))


DEFAULTINFOTABLESTYLE = [
    ("TEXTCOLOR", (1, 0), (-1, 0), colors.gray),
    ("FONT", (0, 0), (-1, -1), "Calibri", 8),
    ("FONT", (1, 1), (-1, 1), "Calibri-Bold", 10),
]


def DEFAULTTITLEBLOCKTABLESTYLE(lines):
    style = [
        ("LINEABOVE", (0, 0), (-1, 0), 3, colors.black),  # topline
        ("LINEBELOW", (0, -1), (-1, -1), 3, colors.black),  # bottomline
        ("SPAN", (0, 0), (2, -1)),
        ("SPAN", (3, 1), (5, 1)),  # client
        ("SPAN", (3, 5), (5, 5)),  # status
        ("SPAN", (6, 1), (8, 3)),  # project
        ("SPAN", (9, 1), (11, 2)),  # document title
        ("SPAN", (9, 4), (11, 4)),  # document number
        ("SPAN", (9, 5), (11, 5)),  # document number
    ]
    for i in range(lines):
        if i % 2 == 0:
            style.append(("FONT", (0, i), (-1, i), "Calibri", 10))
            style.append(("TEXTCOLOR", (0, i), (-1, i), colors.gray))
            style.append(("VALIGN", (1, i), (-1, i), "BOTTOM"))
            style.append(("BOTTOMPADDING", (0, i), (-1, i), 0))
        else:
            style.append(("FONT", (0, i), (-1, i), "Calibri-Bold", 14))
            style.append(("TEXTCOLOR", (0, i), (-1, i), colors.black))
            style.append(("VALIGN", (1, i), (-1, i), "TOP"))
            style.append(("TOPPADDING", (0, i), (-1, i), 0))

    style.append(("BACKGROUND", (0, 0), (2, -1), colors.black))
    style.append(("VALIGN", (0, 0), (0, -1), "MIDDLE"))
    style.append(("LINEBEFORE", (0, 0), (0, -1), 3, colors.black))

    return style


# (COL, ROW)
def DEFAULTTABLESTYLE(defaultcols=4):
    # defaultcols in the number of columns BEFORE "Rev"
    DEFAULTTABLESTYLE = [
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
    return DEFAULTTABLESTYLE


class MFDoc:
    """MF styled pdf document"""

    def __init__(self):
        self.title = "SET document variable .title"
        self.set_page_size(landscape(A3))  # default to A3 size.
        self.address = self.filename = None
        self.pageinfo = "Set document variable pageinfo"
        self.address_compact = []

    def set_page_size(self, pagesize):
        """Page size from reportlab.lib.pagesizes"""
        self.pagesize = pagesize
        self.page_width, self.page_height = self.pagesize
        self.margin, self.bottom_margin = inch, 2.25 * inch

    def go(self, elements, docissue):
        """create the report!"""
        if not self.filename:
            return False
        self.docissue = docissue
        # TODO check can write to file.
        try:
            doc = SimpleDocTemplate(
                self.filename,
                pagesize=self.pagesize,
                leftMargin=self.margin,
                rightMargin=self.margin,
                bottomMargin=self.bottom_margin,
                topMargin=self.margin,
            )
            doc.build(
                elements,
                onFirstPage=self.my_first_page,
                onLaterPages=self.my_later_pages,
            )
        except:
            msg = "Permission denied: {0} \n Make sure it's not open in another program. \n".format(
                self.filename
            )
            logging.warning(msg)
            raise ValueError(msg)

    def my_first_page(self, canvas, doc):
        """Formatting for the first page of the documebt"""
        canvas.saveState()
        self.draw_titleblock(canvas, doc)
        canvas.restoreState()

    def draw_titleblock(self, canvas, doc):
        tab = title_block_table(self.docissue, is_a3=True, office=self.office)
        width, height = self.pagesize
        width = width - 2 * (self.margin + 2 * mm)
        tab.wrapOn(canvas, width, height)
        tab.drawOn(canvas, self.margin, 0.5 * self.margin)

    def my_later_pages(self, canvas, doc):
        """Formatting for the rest of the document includes the footer"""
        canvas.saveState()
        self.draw_titleblock(canvas, doc)
        canvas.restoreState()


def address(mfaddress, elements):
    """print the address"""
    for line in mfaddress:
        elements.append(Paragraph(line, ADDRESSSTYLE))
    return elements


def header(txt, elements, style=HEADERSTYLE2, klass=Paragraph, sep=0.3):
    """write a header"""
    spac = Spacer(0.2 * inch, sep * inch)
    elements.append(spac)
    para = klass(txt, style)
    elements.append(para)
    return elements


def p_nospace(txt, elements, style=PARASTYLE):
    """used for sid header"""
    style = ParagraphStyle(
        name="Normal",
        fontName="Calibri-Bold",
        fontSize=10,
    )
    para = Paragraph(txt, style)
    para = Preformatted(txt, style)
    elements.append(para)
    return elements


def p(txt, elements):
    """write a paragraph of text"""
    return header(txt, elements, style=PARASTYLE, sep=0.1)


def dist_line_style(line):
    sid_style = []
    sid_style.append(("SPAN", (0, line), (-1, line)))
    sid_style.append(("BACKGROUND", (0, line), (-1, line), HIGHLIGHT_COLOUR))
    sid_style.append(("LINEABOVE", (0, line), (-1, line), THICKLINE, colors.black))
    sid_style.append(("LINEBELOW", (0, line), (-1, line), THICKLINE, colors.black))
    sid_style.append(("VALIGN", (0, line), (-1, line), "MIDDLE"))
    sid_style.append(("TOPPADDING", (0, line), (-1, line), 0))
    sid_style.append(("FONT", (0, line), (-1, line), "Calibri-Bold", 16))
    return sid_style


def sid_line_style(line):
    sid_style = []
    sid_style.append(("SPAN", (0, line), (-1, line)))
    sid_style.append(("BACKGROUND", (0, line), (-1, line), HIGHLIGHT_COLOUR))
    sid_style.append(("LINEABOVE", (0, line), (-1, line), THICKLINE, colors.black))
    sid_style.append(("LINEBELOW", (0, line), (-1, line), THICKLINE, colors.black))
    return sid_style


def table(
    data,
    elements,
    tablestyle=DEFAULTTABLESTYLE(),
    col_widths=[100 * mm, 40 * mm, 9 * mm],
):
    """Create the data table"""
    mytable = Table(
        data,
        col_widths + [9 * mm] * 2 + (len(data[1]) - 5) * [7 * mm] + [None],
        repeatRows=NUM_HEADER_ROWS,
        hAlign="LEFT",
        splitByRow=True,
    )
    mytable.setStyle(TableStyle(tablestyle))
    mytable.vAlign = "CENTER"
    elements.append(mytable)
    return elements


def highlight_last_format(data, startrow=0, rev_position=4):
    """highlight the last cell in a row ignores blank cells"""
    formatting = [] + DEFAULTTABLESTYLE(defaultcols=rev_position)
    maxj = -1
    for i, line in enumerate(data):
        if i >= startrow:
            for j, val in enumerate(line):
                try:
                    if line[rev_position] == line[0]:  # distribution list
                        if val:
                            maxj = j
                    elif (
                        val and val == line[rev_position]
                    ):  # line[2] is the current rev
                        maxj = j
                except:
                    print("line doesn't have a current rev: ", line)
            if not line[0] is "":
                formatting.append(("BACKGROUND", (maxj, i), (maxj, i), CURRENT_COLOUR))
    return formatting


@contextmanager
def change_dir(directory):
    current_dir = os.getcwd()
    os.chdir(directory)
    try:
        yield
    finally:
        os.chdir(current_dir)


def issue_sheet(
    data,
    document,
    docissue: DocumentIssue,
    headings=[[""] * 4] * 4,
    tablestyle=DEFAULTTABLESTYLE(),
    col_widths=[100, 40, 9],
    fdir=pathlib.Path("."),
):
    """populate and draw the issue sheet"""

    data2 = headings + data
    document.set_page_size(landscape(A3))

    ###CONTENT###
    Elements = []  ###List of everything in order.
    Elements = table(
        data2, Elements, tablestyle=tablestyle, col_widths=[i * mm for i in col_widths]
    )  # Highlight everything that equals Basement can replace with more sophisticated conditions.
    with change_dir(fdir):
        document.go(Elements, docissue)

    return document
