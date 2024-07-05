import pandas as pd
import pathlib
import math as math
import logging

from frictionless import Package
from textwrap import wrap

from document_issue.document_issue import Issue, DocumentIssue
from .styles import (
    DEFAULTTABLESTYLE,
    register_fonts,
)
from .utils import change_dir
from .constants import (
    address_from_loc,
    address_from_loc_compact,
    DEFAULT_TITLES,
    DEFAULT_COLS,
    MAX_COLS_IN_PART,
)
from .models import LookupData
from .title_block import title_block_table
from .styles import (
    CURRENT_COLOUR,

    NUM_HEADER_ROWS,
    HIGHLIGHT_COLOUR,
    THICKLINE,
    colors,
    PARASTYLE,
    ParagraphStyle,

)
from reportlab.platypus import (
    Table,
    SimpleDocTemplate,
    TableStyle,
    Paragraph,
    Preformatted,
)
from reportlab.lib import colors
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.styles import ParagraphStyle


register_fonts()

logger = logging.getLogger(__name__)


def format_data_rows(rows):
    # rows is a list of list.
    for i, row in enumerate(rows):
        _row = row
        _row[0] = "\n".join(wrap(_row[0], 80))
        rows[i] = _row
    return rows


def cols_to_plot_history(li_issues, part, max_cols_in_part):
    if part > 0:
        startindex = (part - 1) * max_cols_in_part
        endindex = part * max_cols_in_part
        return li_issues[startindex:endindex]
    else:
        return li_issues


def datatable_distribution(
    config,
    issue,
    distribution,
    data_list=[],
    sid_style=[],
    history=False,
    part=-1,
):
    df_distribution = pd.DataFrame(distribution)
    df_distribution_pivot = df_distribution.pivot(
        index="recipient", columns="date_status", values="issue_format"
    )
    li_issues = sorted(list(set([i["date_status"] for i in issue])))

    ###LET's Do the Distribution List

    if history:
        cols_issue = cols_to_plot_history(li_issues, part, MAX_COLS_IN_PART)
    else:
        cols_issue = config["selected_issues"]

    data_list += [[""]]  # blank line
    sid_style += dist_line_style(4 + len(data_list))
    data_list += [["Distribution"]]
    sid_style += dist_line_style(4 + len(data_list))

    doc_dist = df_distribution_pivot.T.to_dict()
    for i in range(len(doc_dist)):
        sid_style.append(
            (
                "SPAN",
                (0, 5 + len(data_list) + i),
                (len(DEFAULT_COLS) - 1, 5 + len(data_list) + i),
            )
        )
    li = []
    for k, v in doc_dist.items():
        li.append([k] * len(DEFAULT_COLS) + [v[c] for c in cols_issue])
    data_list += li

    return data_list, sid_style


def datatable_issue(lookup, config, issue, document, history=False, part=-1):

    df_issue = pd.DataFrame(issue)
    df_issue_pivot = df_issue.pivot(
        index="document_code", columns="date_status", values="revision_number"
    )
    df_document = pd.DataFrame(document)
    docs = list(df_issue.document_code.unique())
    current_revs = {
        d: df_issue.set_index("document_code")
        .loc[d]
        .sort_values("date_status")
        .revision_number.iloc[-1]
        for d in docs
    }
    df_document["Current Rev"] = (
        df_document.document_code.map(current_revs)
        .fillna(0)
        .astype(int)
        .astype(str)
        .str.replace("0", "")
    )

    #
    li_issues = sorted(list(set([i["date_status"] for i in issue])))
    if history:
        cols_issue = cols_to_plot_history(li_issues, part, MAX_COLS_IN_PART)
    else:
        cols_issue = config["selected_issues"]
    cols = DEFAULT_COLS + cols_issue
    last_col = cols[-1]

    df_out = pd.concat(
        [df_document.set_index("document_code"), df_issue_pivot], axis=1
    ).reset_index()

    df_out = df_out.rename(columns={"document_code": "Document Number"})
    df_out = df_out[cols + ["System Identifier Description"]]
    df_out.dropna(subset=cols_issue, inplace=True, how="all")
    for c in cols_issue:
        df_out[c] = df_out[c].fillna(0).astype(int).astype(str).str.replace("0", "")

    data_list = []  # this is a list of rows in the table. #list for styling output.
    sid_style = []

    doc_classifications = list(df_document["System Identifier"].unique())

    for c in doc_classifications:
        sid = lookup.classification[c]
        uniclass = lookup.classification_uniclass[c]

        if uniclass == "N/A":
            uniclass = ""

        df = df_out[df_out["System Identifier Description"] == sid].sort_values(
            "Document Number"
        )
        if len(df) > 0:
            data_list += [[p_nospace("{0}    {1}".format(sid, uniclass), [])]]
            sid_style += sid_line_style(4 + len(data_list))
            data_list += format_data_rows(
                df[cols].values.tolist()
            )  # This is where they get added.
            data_list += [[""] * len(cols)]

    return data_list, sid_style


def tablestyle(history, sid_style, data_list, headings):
    if history:
        _tablestyle = (
            highlight_last_format(
                headings + data_list, startrow=5, rev_position=len(DEFAULT_COLS) - 1
            )
            + sid_style
        )
    else:
        _tablestyle = DEFAULTTABLESTYLE(defaultcols=len(DEFAULT_COLS) - 1) + sid_style
    return _tablestyle


def create_issue_headings(cols_to_plot):
    """format the thing that goes at the top"""
    headings = [
        [""] * len(cols_to_plot) + [""],
        [""] * len(cols_to_plot),
        [""] * len(cols_to_plot),
        [""] * len(cols_to_plot),
        cols_to_plot,
    ]

    for i in range(len(DEFAULT_COLS), len(cols_to_plot)):
        headings[0][i] = cols_to_plot[i][6:8]
        headings[1][i] = cols_to_plot[i][4:6]
        headings[2][i] = cols_to_plot[i][2:4]
        headings[3][i] = cols_to_plot[i][9:]
        headings[4][i] = ""

    for i, string in enumerate(["Day", "Month", "Year", "Status"]):
        headings[i][len(DEFAULT_COLS) - 1] = string

    for i in range(1, len(DEFAULT_TITLES)):
        headings[4][i] = DEFAULT_TITLES[i]
    return headings


def new_document(projectname, office):
    """creates a new Max Fordham document"""
    document = MFDoc()
    document.title = projectname
    document.address = address_from_loc(office)
    document.address_compact = address_from_loc_compact(office)
    document.office = office
    return document


def create_docissue(
    projectinfo, part=0, num_parts=1, history: bool = False
) -> DocumentIssue:
    issue = Issue(
        revision="P01", status_code="S2", status_description="Suitable for information"
    )
    project_number = projectinfo.get("Project Code")

    docissue = DocumentIssue(
        project_name=projectinfo.get("Project Name"),
        project_number=project_number,
        issue_history=[issue],
        name_nomenclature=projectinfo.get("Naming Convention"),
        status_description="Suitable for information",
        roles=[
            dict(role="Director in Charge", initials=projectinfo.get("Project Leader"))
        ],
    )

    if history:
        document_code = "{}-MXF-XX-XX-IS-J-0000{}".format(project_number, part)
        c = "06667-MXF-XX-XX-SH-M-2000{0}".format(part)
        docissue.document_description = f"Issue History: Part {part} of {num_parts}"
        docissue.document_code = document_code
    else:
        document_code = "{}-MXF-XX-XX-IS-J-00100".format(project_number)
        c = "06667-MXF-XX-XX-SH-M-20000".format(part)
        docissue.document_description = f"IssueSheet"
        docissue.document_code = document_code

    return docissue


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
        # try:
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
        # except:
        #     msg = "Permission denied: {0} \n Make sure it's not open in another program. \n".format(
        #         self.filename
        #     )
        #     logging.warning(msg)
        #     raise ValueError(msg)

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
            if not line[0] == "":
                formatting.append(("BACKGROUND", (maxj, i), (maxj, i), CURRENT_COLOUR))
    return formatting


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


def issuesheet_part(
    fdir,
    history,
    part,
    config,
    issue,
    document,
    distribution,
    projectinfo,
    lookup,
    num_parts=1,
):
    li_issues = sorted(list(set([i["date_status"] for i in issue])))
    document_issue_sheet = new_document(
        projectinfo.get("project_name"),
        office=config.get("office"),
    )

    data_list, sid_style = datatable_issue(
        lookup, config, issue, document, history=history, part=part
    )

    data_list, sid_style = datatable_distribution(
        config,
        issue,
        distribution,
        data_list=data_list,
        sid_style=sid_style,
        history=history,
        part=part,
    )

    if history:
        cols_issue = cols_to_plot_history(li_issues, part, MAX_COLS_IN_PART)
    else:
        cols_issue = config["selected_issues"]
    cols_to_plot = DEFAULT_COLS + cols_issue

    issue = Issue(
        revision="P01", status_code="S2", status_description="Suitable for information"
    )
    docissue = create_docissue(projectinfo, part, num_parts, history=history)

    headings = create_issue_headings(cols_to_plot)
    tstyle = tablestyle(history, sid_style, data_list, headings)
    document_issue_sheet.filename = str(pathlib.Path(docissue.document_code + ".pdf"))
    document = issue_sheet(
        data_list,
        document_issue_sheet,
        docissue,
        headings=headings,
        tablestyle=tstyle,
        col_widths=[100, 40, 9],
        fdir=fdir,
    )  # This saves the file to pdf

    return fdir / document_issue_sheet.filename


def write_issuesheet(config, issue, document, distribution, projectinfo, lookup):
    fdir = pathlib.Path(config["outgoing_folder"])
    history = False
    part = -1

    return issuesheet_part(
        fdir, history, part, config, issue, document, distribution, projectinfo, lookup
    )


def write_issuehistory(config, issue, document, distribution, projectinfo, lookup):
    fdir = pathlib.Path(config["outgoing_folder"])
    li_issues = sorted(list(set([i["date_status"] for i in issue])))
    no_issues = len(li_issues)
    history = True

    fpths = []
    if no_issues > MAX_COLS_IN_PART:  # Pagination required.
        num_parts = math.ceil(no_issues / MAX_COLS_IN_PART)
        for part in range(1, num_parts + 1):
            fpths.append(
                issuesheet_part(
                    fdir,
                    history,
                    part,
                    config,
                    issue,
                    document,
                    distribution,
                    projectinfo,
                    lookup,
                    num_parts=num_parts,
                )
            )
    return fpths


def load_datapackage(fdir):
    pkg = Package(fdir / "datapackage.yaml")

    config = pkg.get_resource("config").read_data()
    issue = pkg.get_resource("issue").read_rows()
    document = pkg.get_resource("document").read_rows()
    distribution = pkg.get_resource("distribution").read_rows()
    projectinfo = pkg.get_resource("projectinfo").read_data()
    lookup = LookupData(**pkg.get_resource("lookup").read_data())

    return config, issue, document, distribution, projectinfo, lookup


def write_issuesheet_and_issuehistory(fdir):
    config, issue, document, distribution, projectinfo, lookup = load_datapackage(fdir)
    fpth_issuesheet = write_issuesheet(
        config, issue, document, distribution, projectinfo, lookup
    )
    fpths_issuehistory = write_issuehistory(
        config, issue, document, distribution, projectinfo, lookup
    )
    return fpth_issuesheet, fpths_issuehistory
