import subprocess
import pandas as pd
import pathlib
import json
import os
import webbrowser
import math as math
from reportlab.lib import colors
from textwrap import wrap
import logging
from mf_reportlab.issuesheet_reportlab import issue_sheet
from mf_reportlab.mf_styles import MFDoc, DEFAULTTABLESTYLE, highlight_last_format
from mf_reportlab.mf_styles import p_nospace, get_titleblockimage
from mf_reportlab.mf_styles import dist_line_style, sid_line_style
from constants import (
    address_from_loc,
    address_from_loc_compact,
    OFFICES,
    SHEETTABLEDICT,
    TITLETEXT,
    HIGHLIGHT_COLOUR,
    DEFAULT_TITLES,
    DEFAULT_COLS,
    START_ROW,
    START_COL,
    MAX_COLS_IN_PART,
    CONFIG_DIR,
    DEFAULT_CONFIG,
)
import pathlib
from frictionless import Package, Resource
from frictionless.resources import JsonResource
from models import LookupData

logger = logging.getLogger(__name__)


class BuildIssueSheet:

    @staticmethod
    def cols_to_plot(
        history=False,
        part=-1,
        max_cols_in_part=MAX_COLS_IN_PART,
        selected_issues=[],
        li_issues=[],
    ):
        """get the columns to include in the pdf from the listbox"""

        if part > 0:
            startindex = (part - 1) * max_cols_in_part
            endindex = part * max_cols_in_part
            return DEFAULT_COLS + li_issues[startindex:endindex]

        if history:
            return DEFAULT_COLS + li_issues

        cols = []
        for i in map(int, selected_issues):
            cols.append(li_issues[i])
        return DEFAULT_COLS + cols

    @staticmethod
    def document_number(history, part, project_code, add_space=False):  # TODO: fix this
        """number has the form VWXYZ"""
        VW = "00"  # by definition
        if history:
            if part < 1:
                XYZ = "001"
            elif part < 10:
                XYZ = "00" + str(int(part))
            else:
                XYZ = "0" + str(int(part))
        else:
            # XYZ = str(int(self.listbox.curselection()[0] + 100))
            XYZ = "100"
        doc_numb = project_code + "  -  MXF  -  XX  -  XX  -  IS  -  J  -  " + VW + XYZ
        if not add_space:
            return doc_numb.replace(" ", "")

        # TODO popout to allow custom document number.
        return doc_numb

    @staticmethod
    def construct_title_block(
        history, part, selected_issues, li_issues, projectinfo, config, lookup
    ):
        """title block for the document"""
        d, m, y, s = BuildIssueSheet.day_month_year_status(
            -1, history, selected_issues=selected_issues, li_issues=li_issues
        )
        try:
            status_description = lookup.status[s].split(" - ")[2]
        except:
            status_description = ""
            logger.warning(s + " - status not found in lookup table, consider checking")

        if history:
            part_str = str(part)
            if part_str:
                doc_title = " History: Part " + part_str
            else:
                doc_title = " History"
        else:
            doc_title = "\n" + d + "/" + m + "/" + y + " - " + s
        project_code = projectinfo.get("Project Code")
        data = []
        data.append(
            [
                get_titleblockimage(config["office"]),
                "",
                "",
                "client",
                "",
                "",
                "project",
                "",
                "",
                "document title",
                "",
                "",
            ]
        )
        data.append(
            [
                "",
                "",
                "",
                projectinfo.get("Client Name"),
                "",
                "",
                projectinfo.get("Project Name"),
                "",
                "",
                "Document Issue Sheet" + doc_title,
                "",
                "",
            ]
        )
        data.append(
            [
                "",
                "",
                "",
                "job no.",
                "project leader",
                "scale at A3",
                "",
                "",
                "",
                "",
                "",
                "",
            ]
        )
        data.append(
            [
                "",
                "",
                "",
                projectinfo.get("Job Number"),
                projectinfo.get("Project Leader"),
                "NTS",
                "",
                "",
                "",
                "",
                "",
                "",
            ]
        )
        data.append(
            [
                "",
                "",
                "",
                "status code and description",
                "",
                "",
                "issue date",
                "classification",
                "revision",
                projectinfo.get("Naming Convention"),
                "",
                "",
            ]
        )
        data.append(
            [
                "",
                "",
                "",
                s + status_description,
                "",
                "",
                d + "/" + m + "/" + y,
                "-",
                "-",
                BuildIssueSheet.document_number(
                    history, part, project_code, add_space=True
                ),
                "",
                "",
            ]
        )
        return data

    @staticmethod
    def day_month_year_status(index, history, selected_issues=[], li_issues=[]):
        cols_to_plot = BuildIssueSheet.cols_to_plot(
            history=history, selected_issues=selected_issues, li_issues=li_issues
        )[index]
        d = cols_to_plot[6:8]
        m = cols_to_plot[4:6]
        y = cols_to_plot[2:4]
        s = cols_to_plot[9:]
        return d, m, y, s

    @staticmethod
    def data_table(
        history, part, selected_issues, li_issues, data, doc_descriptions, lookup
    ):

        pkg = Package(
            pathlib.Path(r"J:\J4321\Data\document_issue\config\J3870\datapackage.yaml")
        )
        lookup = LookupData(**pkg.get_resource("lookup").read_data())
        config = pkg.get_resource("config").read_data()
        issue = pkg.get_resource("issue").read_rows()
        document = pkg.get_resource("document").read_rows()

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
        if history:
            cols_issue = sorted(list(set([i["date_status"] for i in issue])))
            if part > 0:
                startindex = (part - 1) * MAX_COLS_IN_PART
                endindex = part * MAX_COLS_IN_PART
            cols_issue = li_issues[startindex:endindex]
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

        doc_classifications = list(
            set([d["System Identifier"] for d in doc_descriptions.values()])
        )

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
        check = data_list
        check1 = sid_style

        # --- old code ---

        # cols = BuildIssueSheet.cols_to_plot(
        #     history=history,
        #     selected_issues=selected_issues,
        #     li_issues=li_issues,
        #     part=part,
        # )
        # last_col = cols[-1]
        # data_tmp = data.sort_values("System Identifier Description")
        # data_list = []  # this is a list of rows in the table. #list for styling output.
        # sid_style = []

        # doc_classifications = list(
        #     set([d["System Identifier"] for d in doc_descriptions.values()])
        # )

        # for c in doc_classifications:
        #     sid = lookup.classification[c]
        #     uniclass = lookup.classification_uniclass[c]

        #     if uniclass == "N/A":
        #         uniclass = ""

        #     df = data_tmp[data_tmp["System Identifier Description"] == sid].sort_values(
        #         "Document Number"
        #     )
        #     if history:
        #         mask = df["Current Rev"].str.len() > 0
        #     else:
        #         mask = df[last_col].str.len() >= 1

        #     if df.loc[mask, cols].values.tolist():
        #         data_list += [[p_nospace("{0}    {1}".format(sid, uniclass), [])]]
        #         sid_style += sid_line_style(4 + len(data_list))
        #         data_list += format_data_rows(
        #             df.loc[mask, cols].values.tolist()
        #         )  # This is where they get added.
        #         data_list += [[""] * len(cols)]

        return data_list, sid_style

    @staticmethod
    def tablestyle(history, sid_style, data_list, headings):
        if history:
            tablestyle = (
                highlight_last_format(
                    headings + data_list, startrow=5, rev_position=len(DEFAULT_COLS) - 1
                )
                + sid_style
            )
        else:
            tablestyle = (
                DEFAULTTABLESTYLE(defaultcols=len(DEFAULT_COLS) - 1) + sid_style
            )
        return tablestyle

    @staticmethod
    def distribution_table(
        doc_distribution,
        data_list,
        sid_style,
        history,
        part,
        selected_issues,
        li_issues,
    ):
        ###LET's Do the Distribution List

        cols = BuildIssueSheet.cols_to_plot(
            history=history,
            selected_issues=selected_issues,
            li_issues=li_issues,
            part=part,
        )
        cols_issues = [x for x in cols if not x in DEFAULT_COLS]

        data_list += [[""]]  # blank line
        sid_style += dist_line_style(4 + len(data_list))
        data_list += [["Distribution"]]
        sid_style += dist_line_style(4 + len(data_list))

        doc_dist = doc_distribution.T.to_dict()
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
            li.append([k] * len(DEFAULT_COLS) + [v[c] for c in cols_issues])
        data_list += li

        return data_list, sid_style

    @staticmethod
    def create_heading(cols_to_plot):
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

    @staticmethod
    def output_doc(
        document,
        fname,
        data,
        doc_distribution,
        projectinfo,
        config,
        doc_descriptions,
        lookup,
        history=False,
        part=-1,
        selected_issues=[],
        column_widths=[100, 40, 9],
        li_issues=[],
    ):

        document.filename = fname
        if not document.filename:
            return False
        # data_list is a list of lists containing the cells of the final table.
        # sid_style is the additional styling applied to the cells over and above the standard.

        data_list, sid_style = BuildIssueSheet.data_table(
            history, part, selected_issues, li_issues, data, doc_descriptions, lookup
        )
        cols_to_plot = BuildIssueSheet.cols_to_plot(
            history=history,
            selected_issues=selected_issues,
            li_issues=li_issues,
            part=part,
        )
        headings = BuildIssueSheet.create_heading(cols_to_plot)
        data_list, sid_style = BuildIssueSheet.distribution_table(
            doc_distribution,
            data_list,
            sid_style,
            history,
            part,
            selected_issues,
            li_issues,
        )
        titleblockdata = BuildIssueSheet.construct_title_block(
            history, part, selected_issues, li_issues, projectinfo, config, lookup
        )
        tstyle = BuildIssueSheet.tablestyle(history, sid_style, data_list, headings)
        document = issue_sheet(
            data_list,
            document,
            titleblockdata=titleblockdata,
            headings=headings,
            tablestyle=tstyle,
            col_widths=column_widths[:3],
        )  # This saves the file to pdf
        return True

    @staticmethod
    def print_issue_and_issue_history(
        data,
        doc_distribution,
        projectinfo,
        lookup,
        config,
        doc_descriptions,
        selected_issues,
        column_widths,
        project_name,
        office,
        max_cols_in_part,
        li_issues,
        project_code,
    ) -> tuple[str, str]:
        filescreated = []
        document = new_document(project_name, office)
        no_issues = len(li_issues)
        # output doc.

        p = pathlib.Path(config["filepath"])
        fdir = p.parent
        savefilename = str(fdir / f"{project_code}-IssueSheet.pdf")
        savefilenamehistory = str(fdir / f"{project_code}-IssueSheethistory.pdf")
        # savefilename = getsavefilename(extension="pdf", initialfile="IssueSheet.pdf")
        # savefilenamehistory = savefilename.replace(".pdf", "_history " + BuildIssueSheet.document_number(True, -1, project_code) + ".pdf")
        fname = savefilename.replace(
            ".pdf",
            " " + BuildIssueSheet.document_number(False, -1, project_code) + ".pdf",
        )

        # output issue sheet
        if not BuildIssueSheet.output_doc(
            document,
            fname,
            data,
            doc_distribution,
            projectinfo,
            config,
            doc_descriptions,
            lookup,
            selected_issues=selected_issues,
            li_issues=li_issues,
            column_widths=column_widths,
        ):
            return False
        else:
            filescreated.append(
                savefilename.replace(
                    ".pdf",
                    " "
                    + BuildIssueSheet.document_number(False, -1, project_code)
                    + ".pdf",
                )
            )

        # continue to output issue istory
        # output history
        if no_issues > max_cols_in_part:  # Pagination required.
            num_parts = math.ceil(no_issues / max_cols_in_part)
            for part in range(1, num_parts + 1):
                fname = savefilename.replace(
                    ".pdf",
                    "_history "
                    + BuildIssueSheet.document_number(True, part, project_code)
                    + ".pdf",
                )
                if not BuildIssueSheet.output_doc(
                    document,
                    fname,
                    data,
                    doc_distribution,
                    projectinfo,
                    config,
                    doc_descriptions,
                    lookup,
                    history=True,
                    part=part,
                    selected_issues=selected_issues,
                    li_issues=li_issues,
                    column_widths=column_widths,
                ):
                    return False
                else:
                    filescreated.append(fname)
            savefilenamehistory = filescreated[-1]
        else:
            if not BuildIssueSheet.output_doc(
                document,
                savefilenamehistory,
                data,
                doc_distribution,
                projectinfo,
                config,
                doc_descriptions,
                lookup,
                history=True,
                selected_issues=selected_issues,
                li_issues=li_issues,
                column_widths=column_widths,
            ):
                return False
            else:
                filescreated.append(savefilenamehistory)

        return filescreated


def new_document(projectname, office):
    """creates a new Max Fordham document"""
    document = MFDoc()
    document.title = projectname
    document.address = address_from_loc(office)
    document.address_compact = address_from_loc_compact(office)
    return document


def config_filename(job_number):
    """return the filename of the config files."""
    # username = os.environ['username']
    return CONFIG_DIR + "\\" + str(job_number) + ".json"


def user_config(job_number):
    """loads the user configuration"""
    file = config_filename(job_number)
    try:
        if os.path.isfile(file):
            with open(file, "r") as handle:
                # config = pickle.load(handle)
                config = json.load(handle)
        else:
            config = DEFAULT_CONFIG
    except:
        logger.warning(
            "Cannot read Job Settings. We'll carry on anyway but contact support.",
            "Config error",
        )

    config = verify_config(config)
    return config


def verify_config(config):
    for k in DEFAULT_CONFIG.keys():
        if k not in config:
            config[k] = DEFAULT_CONFIG[k]
    return config


def save_config(config):
    """save the config (which is a dict) to a file"""

    fpth = pathlib.Path(CONFIG_DIR) / config["job_number"] / "config.json"
    fpth.write_text(json.dumps(config, sort_keys=True, indent=4))

    file = config_filename(config["job_number"])
    try:
        with open(file, "w") as handle:
            # pickle.dump(config, handle)
            print(config)
            print(file)
            json.dump(config, handle, sort_keys=True, indent=4)
    except Exception as e:
        print(e)
        logger.warning(
            "Cannot Save your User Settings. We'll carry on anyway but contact support.",
            "Config error",
        )


def format_data_rows(rows):
    # rows is a list of list.
    for i, row in enumerate(rows):
        _row = row
        _row[0] = "\n".join(wrap(_row[0], 80))
        rows[i] = _row
    return rows


# def read_frictionless()
