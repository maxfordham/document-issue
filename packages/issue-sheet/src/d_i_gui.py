# -*- coding: utf-8 -*-
"""
Created on Tue May 14 13:37:03 2019

@author: o.beckett
"""

import time
import re
from d_i_functions import *
#from mf_modules.tool_usage_tracking import click
import tkinter
from tkinter import END, RIGHT, LEFT, EXTENDED, MULTIPLE, Scrollbar, VERTICAL, Y, X, BOTH, Text, Entry, BOTTOM
from textwrap import wrap

def run():
    ''' go go go!!!!'''
    main_window = DialogWindow(None)
    main_window.mainloop()
    return True

def generate_numbers(jn):
    main_window = NumGeneratorWindow(None, jn)
    main_window.mainloop()
    return True

class NumGeneratorWindow(MFTk):

    def __init__(self, parent, jn):
        MFTk.__init__(self, parent)
        self.title("Document Number Generation")
        self.sheettabledict = SHEETTABLEDICT
        self.revisiontable = get_pandas_data() 
        self.data = {}
        self.job_number = jn
        try:
            for l in self.sheettabledict:
                self.data[l[0]] = table_info(l[0], l[1], l[2])
            self.listboxes = []
            self.initialise()
        except:
            warning_messagebox("Document Number Generation only available in more recent versions of the spreadsheet", "Document Generator Error")
            self._quit()

    def generate(self):
        #click("compare_docs", "DocumentIssue", self.job_number_as_int())
        numdocs = len(self.revisiontable)
        createddocs = 0
        vals = []
        for i, line in enumerate(self.sheettabledict):
            headerrow = index_of_value(line[3], '1. Document Numbering')[0]
            selected = self.listboxes[i].curselection()
            if len(selected) == 0: warning_messagebox("Nothing selected in " + line[0])
            new_val = []
            if line[2]: #dealing with a dict
                keys = self.data[line[0]].keys()
                for s in selected:
                    k = list(keys)[s]
                    if line[0] == "drwgType":
                        new_val.append(k)
                    else:
                        new_val.append(self.data[line[0]][k])
                vals.append(new_val)
            else:
                index = self.data[line[0]].index
                for s in selected:
                    #hard code some exceptions
                    if line[0] == "classification":
                        new_val.append(self.data[line[0]]['classification_des'][s])
                    else:
                        new_val.append(index[s])
                vals.append(new_val)
            
        for item in product(*vals):
            add_doc(headerrow + createddocs + numdocs, self.sheettabledict, item)
            createddocs += 1
        #click("generate_numbers", "DocumentIssue", self.jn)

    def initialise(self):
        ### Banner ###
        #MFHeader(self, text="Generate Numbers").pack(fill=BOTH)
        MFButton(self, text="Generate Document Numbers", command=self.generate).pack(side=BOTTOM, fill=X)
        for i, line in enumerate(reversed(self.sheettabledict)):
            scrollbar = Scrollbar(self, orient=VERTICAL)
            self.listboxes.insert(0, tkinter.Listbox(master=self,
                                        height=50,
                                        selectmode=MULTIPLE,
                                        yscrollcommand=scrollbar.set,
                                        exportselection=0)
                                )
            scrollbar.config(command=self.listboxes[0].yview)
            scrollbar.pack(side=RIGHT, fill=Y)
            self.listboxes[0].pack(side=RIGHT, fill=X)
            if line[2]:
                d = self.data[line[0]]
                for k in d.keys():
                    self.listboxes[0].insert(END, str(k) + " - " + str(d[k]))
            else:
                d = self.data[line[0]]
                for k, item in enumerate(d.index):
                    self.listboxes[0].insert(END, str(item) + " - " + str(d[d.columns[-1]][k]))

        
        self.protocol("WM_DELETE_WINDOW", self._quit) #Overide close event.

    def _quit(self):
        self.quit()     # stops mainloop
        self.destroy()  # this is necessary on Windows to prevent...
        
        
# get data from the spreadsheet
class IssueSheet:
    def __init__(self):
        pass


class GetData:
    def __init__(self):
        self.projectinfo = project_info()
        self.config = user_config(self.projectinfo.get("Job Number"))
        self.data = get_pandas_data()
        self.li_issues = self.get_issues()
        self.dist_data = get_distribution_data(li_issues=self.li_issues)
        
        
    def get_issues(self):
        '''work out which columns are dates'''
        match_str = r"^20(\d{2}\d{2}\d{2})-.*$" # string match date format 20YYMMDD-...
        #                                       ^ Test here: https://regex101.com/r/qH0sU7/1
        return [c for c in self.data.columns if re.match(match_str, c) is not None]



### THE INTERFACE fpor the wizard###
class DialogWindow(MFTk):
    ''' This is the window that will appear on top of excel to control saving
        of the pdf document'''

    def __init__(self, parent):
        MFTk.__init__(self, parent)
        data = GetData()
        self.title("Document Issue")
        self.parent = parent
        self.projectinfo = project_info()
        self.config = user_config(self.get_project_info("number"))  # persistent user settings... don't think this works
        self.data = get_pandas_data()
        self.headers = self.data.columns
        self.dist_data = get_distribution_data()
        self.fix_dist_data()
        self.document = new_document(self.get_project_info("Project Name"), self.config)
        self.col_widths = tkinter.StringVar(self)
        try: #try for backwards compat.
            cw = self.config["col_widths"]
        except:
            cw = "100,40,9"
        self.col_widths.set(cw)
        self.max_cols_in_part = tkinter.IntVar(self)
        try:
            self.max_cols_in_part.set(self.config["max_cols_in_part"])
        except:
            self.max_cols_in_part.set(MAX_COLS_IN_PART)
        self.lookupdata = {} #table containing all the lookup tables
        try:
            for l in SHEETTABLEDICT:
                self.lookupdata[l[0]] = table_info(l[0], l[1], l[2])
        except:
            pass
        self.open_on_save = tkinter.BooleanVar(self)
        self.open_on_save.set(self.config["open_on_save"])
        self.check_on_save = tkinter.BooleanVar(self)
        self.check_on_save.set(self.config["check_on_save"])
        self.outgoingfolder = ""
        self.sid_info = sid_info()
        self.status_info = status_info()
        self.last_col = None
        self.initialise()
        self.protocol("WM_DELETE_WINDOW", self._quit) #Ovveride close event.

        #click("run", "DocumentIssue", self.job_number_as_int())

    def job_number_as_int(self):
        jn = self.get_project_info("number")
        try:
            return int(jn.lower().replace("j", ""))
        except:
            return 4321

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
            warning_messagebox(message="Could not find value: " + str(key) + ". Consider adding it to the project info on the readme tab.", title="Project Info Key error.")
            return "-"

    def dates(self):
        '''work out which columns are dates'''
        match_str = r"^20(\d{2}\d{2}\d{2})-.*$" # string match date format 20YYMMDD-...
        #                                       ^ Test here: https://regex101.com/r/qH0sU7/1
        return [c for c in self.headers if re.match(match_str, c) is not None]

    def fix_dist_data(self):
        try:
            cols = list(self.dist_data.columns)
            for i, col in enumerate(self.dates()): 
                cols[i] = col
            self.dist_data.columns = cols
            df = self.dist_data[self.dates()+["Name"]]
            self.dist_data = df.loc[df.index.notnull()]
        except:
            warning_messagebox(message="Something has gone wrong with your distribution table. You probably haven't expanded it to the correct size to match the document revision information.", title="Distribution Table Error")
            self._quit()

    def cols_to_plot(self, history=False, part=-1):
        '''get the columns to include in the pdf from the listbox'''

        if part>0:
            startindex = (part-1)*self.max_cols_in_part.get()
            endindex = part*self.max_cols_in_part.get()
            return DEFAULT_COLS + self.dates()[startindex:endindex]

        if history: 
            return DEFAULT_COLS + self.dates()

        cols = []
        for i in map(int, self.listbox.curselection()):
            cols.append(self.dates()[i])
        return DEFAULT_COLS + cols

    def document_number(self, history, part, add_space=False):  # TODO: fix this
        ''' number has the form VWXYZ '''
        VW = "00" #by definition
        if history:
            if part < 1: XYZ = "001"
            elif part<10: XYZ = "00" + str(int(part))
            else: XYZ = "0" + str(int(part))
        else:
            XYZ = str(int(self.listbox.curselection()[0] + 100))
        doc_numb = self.get_project_info("Project Code") + "  -  MXF  -  XX  -  XX  -  IS  -  J  -  " + VW + XYZ
        if not add_space: 
            return doc_numb.replace(" ", "")

        #TODO popout to allow custom document number.
        return doc_numb

    def generate_numbers(self):
        generate_numbers(self.job_number_as_int())

    def initialise(self):
        '''create the interface'''
        ### Banner ###
        MFHeader(self, text="Document Issue").pack(fill=BOTH)
        MFLabelBlack(self, text=TITLETEXT).pack(fill=BOTH)
        MFButton(text="Help ‽", command=gotohelp, width=10).pack(fill=BOTH)

        ###Import/Generate Doc Numbers###
        numberconfig = MFLabelFrame(self, text="Import/Generate Doc Numbers", padx=5, pady=5)
        numberconfig.pack(fill=X)
        MFButton(master=numberconfig, text="Generate Doc Numbers", command=self.generate_numbers, width=25).pack(side=BOTTOM)
        #MFButton(master=numberconfig, text="Import from Revit", command=self.import_from_revit, width=25).pack(side=BOTTOM)

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
        self.listbox = tkinter.Listbox(master=groupoptions,
                                       selectmode=EXTENDED,
                                       yscrollcommand=scrollbar.set)
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
        MFButton(master=groupfolder, text="...", command=self.get_outgoingfolder, width=3).pack(side=LEFT)

        ### Save/Quit ###
        groupplot = MFLabelFrame(self, text="Save", padx=5, pady=5)
        groupplot.pack(fill=X)
        frame1 = tkinter.Frame(master=groupplot)
        frame1.pack()
        frame2 = tkinter.Frame(master=groupplot)
        frame2.pack()
        MFCheckButton(master=frame2,
                              text="Open document after save",
                              variable=self.open_on_save, width=40).pack(side=tkinter.BOTTOM)
        MFCheckButton(master=frame2,
                                   text="Check documents before save",
                                   variable=self.check_on_save, width=40).pack(side=tkinter.BOTTOM)
        MFButton(master=frame1, text="Save", command=self.save, width=10).pack(side=LEFT)
        MFButton(master=frame1, text="Quit", command=self._quit, width=10).pack(side=LEFT)
        MFButton(master=frame1, text="Check Docs", command=self.compare_docs, width=10).pack(side=LEFT)


        ### Errors ###
        MFLabelFrame(self, text="Errors", padx=15, pady=15).pack()

    def update_config(self):
        try:
            '''save the user configs to Y:'''
            self.config['job_number'] = self.get_project_info("number")
            self.config["office"] = self.office.get()
            self.config["open_on_save"] = self.open_on_save.get()
            self.config["check_on_save"] = self.check_on_save.get()
            self.config["col_widths"] = self.col_widths.get()
            self.config["max_cols_in_part"] = self.max_cols_in_part.get()
            self.config["filepath"] = xw.Book.caller().fullname
            if  os.environ['username'] not in self.config["users"]:
                self.config["users"].append(os.environ['username'])
            self.config["timestamps"].append(time.strftime("%b %d %Y %H:%M:%S", time.localtime()))
            save_config(self.config)
        except:
            pass

    def construct_title_block(self, history, part):
        ''' title block for the document'''
        d, m, y, s = self.day_month_year_status(-1, history)
        try:
            status_description = " - " + str(self.status_info[self.status_info["status_code"]==s]["Description"][0])
        except:
            status_description = ""
            warning_messagebox(s + " - status not found in lookup table, consider checking", "Status Warning")

        if history:
            part_str = self.get_project_info("Part")
            if part_str:
                doc_title = " History: Part " + part_str
            else:
                doc_title = " History"
        else:
            doc_title = "\n" + d + "/" + m + "/" + y + " - " + s

        data = []
        data.append([get_titleblockimage(self.config['office']), "", "", "client", "", "", "project", "", "", "document title", "", ""])
        data.append(["", "", "", self.get_project_info("Client Name"), "", "", self.get_project_info("Project Name"), "", "", "Document Issue Sheet" + doc_title, "", ""])
        data.append(["", "", "", "job no.", "project leader", "scale at A3", "", "", "", "", "", ""])
        data.append(["", "", "",  self.get_project_info("Job Number"), self.get_project_info("Project Leader") ,"NTS", "", "", "", "", "", ""])
        data.append(["", "", "", "status code and description", "", "", "issue date", "classification", "revision", self.get_project_info("Naming Convention"), "", ""])
        data.append(["", "", "", s + status_description, "", "", d + "/" + m + "/" + y, "-", "-", self.document_number(history, part, add_space=True), "", ""])
        return data

    def get_outgoingfolder(self):
        ''' user select the outgoing folder'''
        try:
            jn = str(self.get_project_info("Job Number"))
            if jn[0].lower() == "j":
                jn = "J:\\" + jn + "\\Outgoing\\"
            else:
                jn = "J:\\J" + jn + "\\Outgoing\\"
        except:
            jn = None

        self.outgoingfolder = getfoldername(initialdir=jn)
        self.folder_text.delete('1.0', END) #clear the text box
        self.folder_text.insert(END, self.outgoingfolder)

    def file_in_data(self, basename):
        ''' check if document is included in issue sheet'''
        return basename in list(self.data["Document Number"])

    def data_in_folder(self, data, filelist):
        ''' check all files in data are in filelist'''
        flist = []
        for file in filelist:
            flist.append(os.path.basename(file).split(".")[0])
        return data in flist

    def compare_docs(self):
        ''' check that all the files that are in the issue sheet are in the outgoing folder'''
        #click("compare_docs", "DocumentIssue", self.job_number_as_int())
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

        cols = self.cols_to_plot(False)
        self.last_col = last_col = cols[-1]
        if last_col not in self.dates(): warning_messagebox("No Specific Issue selected", "Input error")
        mask = self.data[last_col].str.len() >= 1
        for doc in list(self.data.loc[mask,cols]["Document Number"]):
            if not doc in ok_docs:
                if self.data_in_folder(doc, filelist):
                    ok_docs.append(doc)
                else:
                    missing_from_outgoing.append(doc)

        numfiles = len(ok_docs) + len(missing_from_issue) + len(missing_from_outgoing)
        self.compare_docs_message(ok_docs, missing_from_issue, missing_from_outgoing, numfiles)
        return True

    def compare_docs_message(self, ok_docs, missing_from_issue, missing_from_outgoing, numfiles):
        msg = str(len(ok_docs)) + "/" + str(numfiles) + ": OK\n"
        msg += str(len(missing_from_issue)) + "/" + str(numfiles) + ": Missing from issue sheet:\n\t"
        msg += "\n\t".join(missing_from_issue) + "\n"
        msg += str(len(missing_from_outgoing)) + "/" + str(numfiles) + ": Missing from outgoing folder:\n\t"
        msg += "\n\t".join([str(m) for m in missing_from_outgoing])
        msg += "\n\nN.B. this check does not consider file extensions."
        warning_messagebox(message=msg, title="Document Check Results")

    def day_month_year_status(self, index, history):
        cols_to_plot = self.cols_to_plot(history=history)[index]
        d = cols_to_plot[6:8]
        m = cols_to_plot[4:6]
        y = cols_to_plot[2:4]
        s = cols_to_plot[9:]
        return d, m, y, s

    def output_doc(self, fname, history=False, part=-1):

        self.document.filename = fname
        if not self.document.filename: 
            return False
        #data_list is a list of lists containing the cells of the final table.
        #sid_style is the additional styling applied to the cells over and above the standard.
        data_list, sid_style = self.data_table(history, part)
        headings = self.create_heading(self.cols_to_plot(history=history, part=part))
        try:
            data_list, sid_style = self.distribution_table(data_list, sid_style, history, part)
        except Exception as exc:
            message = "Potential problem with distribution table - expand manually to be same size as Revisions table \n"
            warning_messagebox(message=message+str(exc), title="Distribution Table Error")
            return False
        cw = self.get_column_widths()
        projectinfo_list = self.project_info_list()
        titleblockdata = self.construct_title_block(history=history, part=part)
        tstyle = self.tablestyle(history, sid_style, data_list, headings)
        self.document = issue_sheet(data_list,
                                        self.document,
                                        infodata=projectinfo_list,
                                        titleblockdata = titleblockdata,
                                        headings=headings,
                                        tablestyle=tstyle,
                                        col_widths = cw[:3])
        try:
            pass
        except Exception as exc:
            warning_messagebox(message=exc, title="PDF Creation Error")
            return False
        return True

    def project_info_list(self):
        ''' unused '''
        titles = ["project code", "project name", "project address"]
        infodata = [[self.document.address_compact[0]]+titles]
        dictvalues = ["Project Code", "Project Name", "Project Address"]
        dv = [self.get_project_info(i) for i in dictvalues]
        infodata.append([self.document.address_compact[1]] + dv)
        infodata.append([self.document.address_compact[2], "", "", ""])
        return infodata

    def data_table(self, history, part):
        cols = self.cols_to_plot(history=history, part=part)
        self.last_col = last_col = cols[-1]
        data_tmp = self.data.sort_values("System Identifier Description")
        data_list = [] #this is a list of rows in the table. #list for styling output.
        sid_style = []

        df_cat = self.data[["System Identifier", "uniclass"]].set_index("System Identifier")
        for isid, uniclass in enumerate(self.sid_info['uniclass_classification']):
        # for isid, uniclass in enumerate(df_cat):
            sid = self.sid_info['classification_des'].iloc[isid]
            if uniclass == "N/A": 
                uniclass = ""

            df = data_tmp[data_tmp["System Identifier Description"] == sid].sort_values('Document Number')
            if history: 
                mask = df["Current Rev"].str.len() > 0
            else: 
                mask = df[last_col].str.len() >= 1

            if df.loc[mask, cols].values.tolist():
                data_list += [[p_nospace("{0}    {1}".format(sid,uniclass), [])]]
                sid_style += sid_line_style(4+len(data_list))
                data_list += format_data_rows(df.loc[mask, cols].values.tolist()) #This is where they get added.
                data_list += [[""]*len(cols)]

        return data_list, sid_style

    def tablestyle(self, history, sid_style, data_list, headings):
        if history:
            tablestyle = highlight_last_format(headings+data_list, startrow=5, rev_position=len(DEFAULT_COLS)-1) + sid_style
        else:
            tablestyle = DEFAULTTABLESTYLE(defaultcols = len(DEFAULT_COLS)-1) + sid_style
        return tablestyle

    def distribution_table(self, data_list, sid_style, history, part):
        ###LET's Do the Distribution List
        cols = self.cols_to_plot(history=history, part=part)
        data_list += [[""]] #blank line
        sid_style += dist_line_style(4+len(data_list))
        data_list += [["Distribution"]]
        sid_style += dist_line_style(4+len(data_list))
        distcols = ['Name']*len(DEFAULT_COLS) + [x for x in cols if not x in DEFAULT_COLS]

        for i, line in enumerate(self.dist_data[distcols].values.tolist()):
            sid_style.append(('SPAN', (0, 5+len(data_list)+i), (len(DEFAULT_COLS)-1, 5+len(data_list)+i)))

        data_list += self.dist_data[distcols].values.tolist()
        return data_list, sid_style

    def get_column_widths(self):
        cw = self.col_widths.get()
        try: cw = list(map(int,cw.split(",")))
        except Exception as exc: warning_messagebox(message=exc, title="Column Width Error")
        if len(cw) != 3: warning_messagebox(message="Must define three columns widths separated by a comma", title="Column Width Error")
        return cw

    def save(self):
        ''' create and save the pdf file'''
        
        
        self.update_config()
        if self.check_on_save.get():
            if not self.compare_docs(): 
                return False

        filescreated = []
        #output doc.
        self.savefilename = getsavefilename(extension="pdf", initialfile="IssueSheet.pdf")
        self.savefilenamehistory = self.savefilename.replace(".pdf", "_history " + self.document_number(True, -1) + ".pdf")
        if not self.output_doc(self.savefilename.replace(".pdf", " " + self.document_number(False, -1) + ".pdf")): 
            return False
        else: 
            filescreated.append(self.savefilename.replace(".pdf", " " + self.document_number(False, -1) + ".pdf"))

        #output history
        if len(self.dates())>self.max_cols_in_part.get(): #Pagination required.
            num_parts = math.ceil(len(self.dates())/self.max_cols_in_part.get())
            for part in range(1, num_parts+1):
                self.projectinfo['Part'] = str(part) + " of " + str(num_parts)
                fname = self.savefilename.replace(".pdf", "_history " + self.document_number(True, part) + ".pdf")
                if not self.output_doc(fname, history=True, part=part): 
                    return False
                else: 
                    filescreated.append(fname)
            self.savefilenamehistory = filescreated[-1]
        else:
            if not self.output_doc(self.savefilenamehistory, history=True): 
                return False
            else: 
                filescreated.append(self.savefilenamehistory)

        self.create_links(self.cols_to_plot()[-1])
        info_messagebox(message="Documents saved:\n" + "\n".join(filescreated))
        if self.open_on_save.get():
            for file_created in filescreated:
                show_file(file_created)

        #click("create_pdf", "DocumentIssue", self.job_number_as_int())
        return self.document

    def create_links(self, last_col):
        ''' add some hyperlinks to the spreadsheet'''
        iov = index_of_value("Document Number", '1. Document Numbering')
        excel_col = iov[1] + 1 +list(self.data.columns.values).index(last_col) #add three to get it back on track.
        xw.sheets['1. Document Numbering'].range(iov[0]-3, excel_col).value = "=hyperlink(\"" + self.savefilename + "\", \"IssueSheet\")"
        xw.sheets['1. Document Numbering'].range(iov[0]-2, excel_col).value = "=hyperlink(\"" + self.savefilenamehistory + "\", \"History\")"
        if self.outgoingfolder:
            xw.sheets['1. Document Numbering'].range(iov[0]-1, excel_col).value = "=hyperlink(\"" + self.outgoingfolder + "\", \"Outgoing Folder\")"

    def create_heading(self, cols_to_plot):
        ''' format the thing that goes at the top '''
        headings = [[""]*len(cols_to_plot) + [""],
                    [""]*len(cols_to_plot),
                    [""]*len(cols_to_plot),
                    [""]*len(cols_to_plot),
                    cols_to_plot]

        for i in range(len(DEFAULT_COLS), len(cols_to_plot)):
            headings[0][i] = cols_to_plot[i][6:8]
            headings[1][i] = cols_to_plot[i][4:6]
            headings[2][i] = cols_to_plot[i][2:4]
            headings[3][i] = cols_to_plot[i][9:]
            headings[4][i] = ""

        for i, string in enumerate(["Day", "Month", "Year", "Status"]):
            headings[i][len(DEFAULT_COLS)-1] = string

        for i in range(1, len(DEFAULT_TITLES)):
            headings[4][i] = DEFAULT_TITLES[i]
        return headings

    def import_from_revit(self):
        if len(self.lookupdata.keys()) < 1:
            warning_messagebox("Newer version of the spreadsheet is required", "Import problem")
            return False
        fname = getfilename(filetypes=(("excel files","*.xlsx, .xls"),("all files","*.*")))
        if not fname: return False

        df = pd.read_excel(fname, sheet_name="Printing Sheets")
        headerrow = index_of_value(SHEETTABLEDICT[0][3], '1. Document Numbering')[0] #so we know where to insert the new row
        for i in range(len(df)):
            try:
                item = self.construct_doc_item(df.iloc[i])
                add_doc(headerrow + len(self.data), SHEETTABLEDICT, item)
            except Exception as e:
                warning_messagebox(str(e) + " not found in lookup tables try adding it to the relevant one.", "Import Error")
        #construct items from row in table.
        #click("import_revit", "DocumentIssue", self.job_number_as_int())
        return df

    def add_key(self, line, key):
        rowcol = index_of_value(line[1], line[0])
        rowcol = (rowcol[0] + 1, rowcol[1])
        xw.sheets[line[0]].range(str(rowcol[0])+":" + str(rowcol[0])).api.Insert(xw.constants.InsertShiftDirection.xlShiftToRight)
        xw.sheets[line[0]].range(rowcol).value = str(key)
        rowcol = (rowcol[0], rowcol[1] + 1)
        xw.sheets[line[0]].range(rowcol).value = str(key)
        ###reload
        self.lookupdata[line[0]] = table_info(line[0], line[1], line[2])

    def construct_doc_item(self, item):  # only used by the revit link which is not in use
        #i is a list from excel.
        res = []
        for i, line in enumerate(SHEETTABLEDICT):
            r = ""
            if line[2]: #dealing with a dict
                keys = self.lookupdata[line[0]].keys()
                pandaskey = line[4]
                if pandaskey:
                    d = item[pandaskey]
                    #handle ech one individually.
                    if line[0] == "volume" or line[0] == "level":
                        k = str(d)
                        if len(k) == 1: k = "0" + k
                        if k not in keys: self.add_key(line, k)
                        r = self.lookupdata[line[0]][k]
                    elif line[0] == "drwgType":
                        r = str(d)[-3]
                else: #we have some exceptions
                    if line[0] == "project" or line[0] == "originator":
                        k = list(keys)[-1]
                        r = self.lookupdata[line[0]][k] #get the last one
                    if line[0] == "infoType":
                        r = "Drawing" #revit always will export a drawing.
            else: #we have a dataframe in the lookup table.
                pandaskey = line[4]
                d = item[pandaskey]
                d = str(d).replace("_0", "_00")
                if line[0] == "classification":
                    k = d[:14]
                    data = self.lookupdata[line[0]]
                    selected_row = data[data['uniclass_classification']==k].iloc[0]
                    r = selected_row['classification_des']
                elif line[0] == "sequence":
                    r = str(d)[-2:]
            res.append(r)

        return res

    def _quit(self):
        self.update_config()
        self.quit()     # stops mainloop
        self.destroy()  # this is necessary on Windows to prevent...
