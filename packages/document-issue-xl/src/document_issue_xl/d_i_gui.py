# -*- coding: utf-8 -*-
"""
Created on Tue May 14 13:37:03 2019

@author: o.beckett, j.gunstone
"""

import time
import pathlib
import glob
import os
import xlwings as xw
from d_i_read_excel import read_excel

import tkinter
from tkinter import (
    END,
    RIGHT,
    LEFT,
    EXTENDED,
    Scrollbar,
    VERTICAL,
    Y,
    X,
    BOTH,
    Text,
    Entry,
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

from document_issue_io.issuesheet import write_issuesheet_and_issuehistory
import json
import pandas as pd
from pydantic import BaseModel
import webbrowser
import subprocess
import logging
from constants import MAX_COLS_IN_PART, CONFIG_DIR, DEFAULT_COLS, TITLETEXT
from document_issue_io.constants import OFFICES

DIR_TESTOUTPUTS = pathlib.Path(
    r"C:\engDev\git_mf\document-issue\packages\issue-sheet\tests\outputs"
)

logger = logging.getLogger(__name__)


def config_filename(job_number):
    """return the filename of the config files."""
    # username = os.environ['username']
    return CONFIG_DIR + "\\" + str(job_number) + ".json"


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


def run():
    """go go go!!!!"""
    main_window = DialogWindow(None)
    main_window.mainloop()
    return True


def gotohelp():
    webbrowser.open_new(r"mailto:helpdesk@maxfordham.com")


def show_file(filename):
    """open a file in default program"""
    subprocess.Popen(filename, shell=True)


def dump(di: dict):
    """dump the data to the console"""
    fdir = pathlib.Path(r"dump")
    fdir.mkdir(exist_ok=True)
    li = []
    for k, v in di.items():
        if isinstance(v, dict):
            f = fdir / (k + ".json")
            f.write_text(json.dumps(v, indent=4))
        elif isinstance(v, pd.DataFrame):
            f = fdir / (k + ".csv")
            v.to_csv(f)
        elif isinstance(v, BaseModel):
            f = fdir / (k + ".json")
            f.write_text(v.model_dump_json(indent=4))
        elif isinstance(v, list):
            pass
        else:
            raise ValueError(f"Cannot dump {k} of type {type(v)}")
        li.append(f)
    return li


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


### THE INTERFACE fpor the wizard###
class DialogWindow(MFTk):
    """This is the window that will appear on top of excel to control saving
    of the pdf document"""

    def __init__(self, parent):
        MFTk.__init__(self, parent)
        self.title("Document Issue")
        self.parent = parent
        self.get_data()

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
        if DIR_TESTOUTPUTS.exists():
            self.outgoingfolder = str(DIR_TESTOUTPUTS)

        self.last_col = None
        self.initialise()
        self.protocol("WM_DELETE_WINDOW", self._quit)  # Ovveride close event.

    def get_data(self):
        (
            self.lookup,
            self.projectinfo,
            self.config,
            self.data,
            self.li_issues,
            self.doc_revs,  # doc_issues
            self.doc_descriptions,
            self.doc_issues,
            self.doc_distribution,  # doc_distribution
        ) = read_excel()
        # note. ^ this also dumps datapackage to dir and the data is read from there
        #         to build the output issuesheet.

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
        for item in self.li_issues:
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

    @property
    def fdir_package(self):
        return pathlib.Path(CONFIG_DIR) / self.get_project_info("number")

    def update_config(self):
        # try:
        """save the user configs to Y:"""
        self.config["job_number"] = self.get_project_info("number")
        self.config["selected_issues"] = [
            self.li_issues[l] for l in self.listbox.curselection()
        ]
        self.config["outgoing_folder"] = self.outgoingfolder
        self.config["office"] = self.office.get()
        self.config["open_on_save"] = self.open_on_save.get()
        self.config["check_on_save"] = self.check_on_save.get()
        self.config["col_widths"] = self.col_widths.get()
        self.config["max_cols_in_part"] = self.max_cols_in_part.get()
        # self.config["filepath"] = xw.Book.caller().fullname  # THIS isn't working...
        if os.environ["username"] not in self.config["users"]:
            self.config["users"].append(os.environ["username"])
        self.config["timestamps"].append(
            time.strftime("%b %d %Y %H:%M:%S", time.localtime())
        )
        save_config(self.config)

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

        cols = cols_to_plot(
            history=False,
            selected_issues=self.listbox.curselection(),
            li_issues=self.li_issues,
        )
        self.last_col = last_col = cols[-1]
        if last_col not in self.li_issues:
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
        self.get_data()
        self.update_config()
        if self.check_on_save.get():
            if not self.compare_docs():
                return False
        fpth_issuesheet, fpths_issuehistory = write_issuesheet_and_issuehistory(
            self.fdir_package
        )
        filescreated = [str(f) for f in [fpth_issuesheet] + fpths_issuehistory]
        info_messagebox(message="Documents saved:\n" + "\n".join(filescreated))
        return fpth_issuesheet, fpths_issuehistory

    def _quit(self):
        self.update_config()
        self.quit()  # stops mainloop
        self.destroy()  # this is necessary on Windows to prevent...
