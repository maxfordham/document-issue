# -*- coding: utf-8 -*-
"""
Created on Tue May 14 13:37:03 2019

@author: o.beckett, j.gunstone
"""

import time
import pathlib
import re
import xlwings as xw
from d_i_functions import *
from constants import *
from d_i_read_excel import read_excel

# from mf_modules.tool_usage_tracking import click
import tkinter
from tkinter import (
    END,
    RIGHT,
    LEFT,
    EXTENDED,
    MULTIPLE,
    Scrollbar,
    VERTICAL,
    Y,
    X,
    BOTH,
    Text,
    Entry,
    BOTTOM,
)
from d_i_ui import (
    warning_messagebox,
    info_messagebox,
    getsavefilename,
    getfoldername,
    MFButton,
    MFLabelFrame,
    MFLabel,
    MFLabelBlack,
    getfilename,
    MFHeader,
    MFOptionMenu,
    MFCheckButton,
    MFTk,
)


def run():
    """go go go!!!!"""
    main_window = DialogWindow(None)
    main_window.mainloop()
    return True


### THE INTERFACE fpor the wizard###
class DialogWindow(MFTk):
    """This is the window that will appear on top of excel to control saving
    of the pdf document"""

    def __init__(self, parent):
        MFTk.__init__(self, parent)

        self.title("Document Issue")
        self.parent = parent
        self.projectinfo = project_info()
        self.config = user_config(
            self.get_project_info("number")
        )  # persistent user settings... don't think this works
        self.data = get_pandas_data()
        self.headers = self.data.columns
        self.dist_data = get_distribution_data()
        self.fix_dist_data()

        (
            self.lookup,
            self.projectinfo,
            self.config,
            self.data,
            self.li_issues,
            self.doc_revs,
            self.doc_descriptions,
            self.doc_issues,
            self.dist_data,
        ) = read_excel()

        self.col_widths = tkinter.StringVar(self)
        try:  # try for backwards compat.
            cw = self.config["col_widths"]
        except:
            cw = "100,40,9"
        self.col_widths.set(cw)
        self.max_cols_in_part = tkinter.IntVar(self)
        try:
            self.max_cols_in_part.set(self.config["max_cols_in_part"])
        except:
            self.max_cols_in_part.set(MAX_COLS_IN_PART)

        self.open_on_save = tkinter.BooleanVar(self)
        self.open_on_save.set(self.config["open_on_save"])
        self.check_on_save = tkinter.BooleanVar(self)
        self.check_on_save.set(self.config["check_on_save"])

        self.outgoingfolder = ""
        if pathlib.Path(r"C:\Users\j.gunstone\Desktop\dgn").exists():
            self.outgoingfolder = r"C:\Users\j.gunstone\Desktop\dgn"

        self.sid_info = sid_info()
        self.status_info = status_info()
        self.last_col = None
        self.initialise()
        self.protocol("WM_DELETE_WINDOW", self._quit)  # Ovveride close event.

    def get_project_info(self, key):
        try:
            return str(self.projectinfo[key])
        except:
            if "code" in key.lower() or "number" in key.lower():
                return self.get_project_info("Job Number")
            elif "part" in key.lower():
                return None
            elif "naming" in key.lower():
                return "project code - orig - volume - level - role - number"
            warning_messagebox(
                message="Could not find value: "
                + str(key)
                + ". Consider adding it to the project info on the readme tab.",
                title="Project Info Key error.",
            )
            return "-"

    def dates(self):
        """work out which columns are dates"""
        match_str = r"^20(\d{2}\d{2}\d{2})-.*$"  # string match date format 20YYMMDD-...
        #                                       ^ Test here: https://regex101.com/r/qH0sU7/1
        return [c for c in self.headers if re.match(match_str, c) is not None]

    def fix_dist_data(self):
        try:
            cols = list(self.dist_data.columns)
            for i, col in enumerate(self.dates()):
                cols[i] = col
            self.dist_data.columns = cols
            df = self.dist_data[self.dates() + ["Name"]]
            self.dist_data = df.loc[df.index.notnull()]
        except:
            warning_messagebox(
                message="Something has gone wrong with your distribution table. You probably haven't expanded it to the correct size to match the document revision information.",
                title="Distribution Table Error",
            )
            self._quit()

    def initialise(self):
        """create the interface"""
        ### Banner ###
        MFHeader(self, text="Document Issue").pack(fill=BOTH)
        MFLabelBlack(self, text=TITLETEXT).pack(fill=BOTH)
        MFButton(text="Help ‽", command=gotohelp, width=10).pack(fill=BOTH)

        ###Config information###
        groupconfig = MFLabelFrame(self, text="Config", padx=5, pady=5)
        groupconfig.pack(fill=X)
        self.office = tkinter.StringVar(self)
        self.office.set(self.config["office"])
        MFOptionMenu(groupconfig, self.office, *OFFICES).pack()
        frame1 = tkinter.Frame(master=groupconfig)
        frame1.pack()
        MFLabel(frame1, text="Max. packages in history part:").pack(side=LEFT)
        self.max_cols_in_part_text = Entry(frame1, textvariable=self.max_cols_in_part)
        self.max_cols_in_part_text.pack(side=LEFT)

        ###Formatting###
        groupformat = MFLabelFrame(self, text="Formatting", padx=5, pady=5)
        groupformat.pack(fill=X)
        MFLabel(groupformat, text="Column Widths (mm):").pack(side=LEFT)
        self.col_width_text = Entry(groupformat, textvariable=self.col_widths)
        self.col_width_text.pack(fill=X)

        ### Options ###
        groupoptions = MFLabelFrame(self, text="Options", padx=5, pady=5)
        groupoptions.pack(fill=X)
        MFLabel(groupoptions, text="Dates to issue:").pack(side=LEFT)
        scrollbar = Scrollbar(groupoptions, orient=VERTICAL)
        self.listbox = tkinter.Listbox(
            master=groupoptions, selectmode=EXTENDED, yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox.pack(fill=X)
        for item in self.dates():
            self.listbox.insert(END, item)

        ### Outgoing folder group ###
        groupfolder = MFLabelFrame(self, text="Outgoing Sub-Folder", padx=5, pady=5)
        groupfolder.pack(fill=X)
        MFLabel(groupfolder, text="Folder:").pack(side=LEFT)
        self.folder_text = Text(groupfolder, height=1, width=40)
        self.folder_text.pack(side=tkinter.LEFT)
        MFButton(
            master=groupfolder, text="...", command=self.get_outgoingfolder, width=3
        ).pack(side=LEFT)

        ### Save/Quit ###
        groupplot = MFLabelFrame(self, text="Save", padx=5, pady=5)
        groupplot.pack(fill=X)
        frame1 = tkinter.Frame(master=groupplot)
        frame1.pack()
        frame2 = tkinter.Frame(master=groupplot)
        frame2.pack()
        MFCheckButton(
            master=frame2,
            text="Open document after save",
            variable=self.open_on_save,
            width=40,
        ).pack(side=tkinter.BOTTOM)
        MFCheckButton(
            master=frame2,
            text="Check documents before save",
            variable=self.check_on_save,
            width=40,
        ).pack(side=tkinter.BOTTOM)
        MFButton(master=frame1, text="Save", command=self.save, width=10).pack(
            side=LEFT
        )
        MFButton(master=frame1, text="Quit", command=self._quit, width=10).pack(
            side=LEFT
        )
        MFButton(
            master=frame1, text="Check Docs", command=self.compare_docs, width=10
        ).pack(side=LEFT)
        ### Errors ###
        MFLabelFrame(self, text="Errors", padx=15, pady=15).pack()

    def update_config(self):
        try:
            """save the user configs to Y:"""
            self.config["job_number"] = self.get_project_info("number")
            self.config["office"] = self.office.get()
            self.config["open_on_save"] = self.open_on_save.get()
            self.config["check_on_save"] = self.check_on_save.get()
            self.config["col_widths"] = self.col_widths.get()
            self.config["max_cols_in_part"] = self.max_cols_in_part.get()
            self.config["filepath"] = xw.Book.caller().fullname
            if os.environ["username"] not in self.config["users"]:
                self.config["users"].append(os.environ["username"])
            self.config["timestamps"].append(
                time.strftime("%b %d %Y %H:%M:%S", time.localtime())
            )
            save_config(self.config)
        except:
            pass

    def get_outgoingfolder(self):
        """user select the outgoing folder"""
        try:
            jn = str(self.get_project_info("Job Number"))
            if jn[0].lower() == "j":
                jn = "J:\\" + jn + "\\Outgoing\\"
            else:
                jn = "J:\\J" + jn + "\\Outgoing\\"
        except:
            jn = None

        self.outgoingfolder = getfoldername(initialdir=jn)
        self.folder_text.delete("1.0", END)  # clear the text box
        self.folder_text.insert(END, self.outgoingfolder)

    def file_in_data(self, basename):
        """check if document is included in issue sheet"""
        return basename in list(self.data["Document Number"])

    def data_in_folder(self, data, filelist):
        """check all files in data are in filelist"""
        flist = []
        for file in filelist:
            flist.append(os.path.basename(file).split(".")[0])
        return data in flist

    def compare_docs(self):
        """check that all the files that are in the issue sheet are in the outgoing folder"""
        if not self.outgoingfolder:
            info_messagebox(message="No Outgoing folder selected")
            return False

        filelist = glob.glob(self.outgoingfolder + "\\**", recursive=True)
        ok_docs = []
        missing_from_issue = []
        missing_from_outgoing = []
        for file in filelist:
            filename = os.path.basename(file).split(".")
            basename = filename[0]
            if len(filename) > 1:
                if self.file_in_data(basename):
                    ok_docs.append(basename)
                else:
                    missing_from_issue.append(basename)

        cols = BuildIssueSheet.cols_to_plot(
            history=False,
            selected_issues=self.listbox.curselection(),
            li_issues=self.li_issues,
        )
        self.last_col = last_col = cols[-1]
        if last_col not in self.dates():
            warning_messagebox("No Specific Issue selected", "Input error")
        mask = self.data[last_col].str.len() >= 1
        for doc in list(self.data.loc[mask, cols]["Document Number"]):
            if not doc in ok_docs:
                if self.data_in_folder(doc, filelist):
                    ok_docs.append(doc)
                else:
                    missing_from_outgoing.append(doc)

        numfiles = len(ok_docs) + len(missing_from_issue) + len(missing_from_outgoing)
        self.compare_docs_message(
            ok_docs, missing_from_issue, missing_from_outgoing, numfiles
        )
        return True

    def compare_docs_message(
        self, ok_docs, missing_from_issue, missing_from_outgoing, numfiles
    ):
        msg = str(len(ok_docs)) + "/" + str(numfiles) + ": OK\n"
        msg += (
            str(len(missing_from_issue))
            + "/"
            + str(numfiles)
            + ": Missing from issue sheet:\n\t"
        )
        msg += "\n\t".join(missing_from_issue) + "\n"
        msg += (
            str(len(missing_from_outgoing))
            + "/"
            + str(numfiles)
            + ": Missing from outgoing folder:\n\t"
        )
        msg += "\n\t".join([str(m) for m in missing_from_outgoing])
        msg += "\n\nN.B. this check does not consider file extensions."
        warning_messagebox(message=msg, title="Document Check Results")

    def get_column_widths(self):
        cw = self.col_widths.get()
        try:
            cw = list(map(int, cw.split(",")))
        except Exception as exc:
            warning_messagebox(message=exc, title="Column Width Error")
        if len(cw) != 3:
            warning_messagebox(
                message="Must define three columns widths separated by a comma",
                title="Column Width Error",
            )
        return cw

    def save(self):
        """create and save the pdf file"""
        selected_issues = self.listbox.curselection()
        column_widths = self.get_column_widths()
        project_name = self.get_project_info("Project Name")
        project_code = self.get_project_info("Project Code")
        office = self.config["office"]
        max_cols_in_part = self.max_cols_in_part.get()

        self.update_config()
        if self.check_on_save.get():
            if not self.compare_docs():
                return False

        savefilename = getsavefilename(extension="pdf", initialfile="IssueSheet.pdf")
        savefilenamehistory = savefilename.replace(
            ".pdf",
            "_history "
            + BuildIssueSheet.document_number(True, -1, project_code)
            + ".pdf",
        )
        filescreated = BuildIssueSheet.print_issue_and_issue_history(
            self.data,
            self.dist_data,
            self.projectinfo,
            self.lookup,
            self.config,
            self.doc_descriptions,
            selected_issues,
            column_widths,
            project_name,
            office,
            max_cols_in_part,
            self.li_issues,
            project_code,
        )
        self.savefilename, self.savefilenamehistory = filescreated[0], filescreated[1]

        info_messagebox(message="Documents saved:\n" + "\n".join(filescreated))
        if self.open_on_save.get():
            for file_created in filescreated:
                show_file(file_created)
        return filescreated

    def create_links(self, last_col):  # TODO: delete ... not req. / no one uses it
        """add some hyperlinks to the spreadsheet"""
        iov = index_of_value("Document Number", "1. Document Numbering")
        excel_col = (
            iov[1] + 1 + list(self.data.columns.values).index(last_col)
        )  # add three to get it back on track.
        xw.sheets["1. Document Numbering"].range(iov[0] - 3, excel_col).value = (
            '=hyperlink("' + self.savefilename + '", "IssueSheet")'
        )
        xw.sheets["1. Document Numbering"].range(iov[0] - 2, excel_col).value = (
            '=hyperlink("' + self.savefilenamehistory + '", "History")'
        )
        if self.outgoingfolder:
            xw.sheets["1. Document Numbering"].range(iov[0] - 1, excel_col).value = (
                '=hyperlink("' + self.outgoingfolder + '", "Outgoing Folder")'
            )

    def _quit(self):
        self.update_config()
        self.quit()  # stops mainloop
        self.destroy()  # this is necessary on Windows to prevent...
