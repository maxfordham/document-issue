import subprocess
import os
import sys
import glob
import pathlib
import pickle
import json
import webbrowser
import xlwings as xw
import pandas as pd
import math as math
from itertools import product
from reportlab.lib import colors
from textwrap import wrap
import logging
from mf_reportlab.issuesheet_reportlab import issue_sheet
from mf_reportlab.mf_styles import MFDoc, DEFAULTTABLESTYLE, highlight_last_format
from mf_reportlab.mf_styles import p_nospace, get_titleblockimage
from mf_reportlab.mf_styles import dist_line_style, sid_line_style
from constants import address_from_loc, address_from_loc_compact, OFFICES

logger = logging.getLogger(__name__)

START_ROW = 35 #Default
START_COL = 1 #B
MAX_COLS_IN_PART = 30
CONFIG_DIR = r'J:\J4321\Data\document_issue\config'
DEFAULT_CONFIG = {"job_number": "4321",
                  "office": "Cambridge",#edinburgh; bristol; manchester; cambridge; london;
                  "open_on_save": "False",
                  "check_on_save": "True",
                  "col_widths": "100,40,9",
                  "max_cols_in_part": MAX_COLS_IN_PART,
                  "users": [],
                  "timestamps": [],
                  "filepath": ""}

DEFAULT_COLS = ["Document Title", "Document Number", "docSource", "Scale", "Size", "Current Rev"]
DEFAULT_TITLES = ["Document Title", "Document Number", "Type",
                  "Scale", "Size", "Rev", "Dated Issue Revisions"]

HIGHLIGHT_COLOUR = colors.Color(168/255, 231/255, 255/255, alpha=1.)

TITLETEXT = "Check and create issue sheets.\n v0.2.0 - May19"

SHEETTABLEDICT = [ #sheet, first header, dict?, tableheader, header in revit export
            ["project", "project_code", True, "Project Name", None],
            ["originator", "originator_code", True, "Originator Description", None],
            ["volume", "volume_code", True, "Volume Name", "03. Volume"],
            ["level", "level_code", True, "Level Description", "04. Level"],
            ["infoType", "infoType_code", True, "Information Type Description", None],
            ["classification", "classification_code", False, "System Identifier Description", "07. Classification"],
            ["drwgType", "drwgType_code", True, "X Sequence Number", "08. Number"],
            ["sequence", "sequence_code", False, "YZ Sequence Number", "08. Number"]
        ]



class BuildIssueSheet:

    @staticmethod
    def cols_to_plot(history=False, part=-1, max_cols_in_part=MAX_COLS_IN_PART, selected_issues=[], li_issues=[]):
        '''get the columns to include in the pdf from the listbox'''

        if part>0:
            startindex = (part-1)*max_cols_in_part
            endindex = part*max_cols_in_part
            return DEFAULT_COLS + li_issues[startindex:endindex]

        if history: 
            return DEFAULT_COLS + li_issues

        cols = []
        for i in map(int, selected_issues):
            cols.append(li_issues[i])
        return DEFAULT_COLS + cols

    @staticmethod
    def document_number(history, part, project_code, add_space=False):  # TODO: fix this
        ''' number has the form VWXYZ '''
        VW = "00" #by definition
        if history:
            if part < 1: XYZ = "001"
            elif part<10: XYZ = "00" + str(int(part))
            else: XYZ = "0" + str(int(part))
        else:
            # XYZ = str(int(self.listbox.curselection()[0] + 100))
            XYZ = "100"
        doc_numb = project_code + "  -  MXF  -  XX  -  XX  -  IS  -  J  -  " + VW + XYZ
        if not add_space: 
            return doc_numb.replace(" ", "")

        #TODO popout to allow custom document number.
        return doc_numb
    
    @staticmethod
    def construct_title_block(history, part, selected_issues, li_issues, projectinfo, config, lookup):
        ''' title block for the document'''
        d, m, y, s = BuildIssueSheet.day_month_year_status(-1, history, selected_issues=selected_issues, li_issues=li_issues)
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
        data.append([get_titleblockimage(config['office']), "", "", "client", "", "", "project", "", "", "document title", "", ""])
        data.append(["", "", "", projectinfo.get("Client Name"), "", "", projectinfo.get("Project Name"), "", "", "Document Issue Sheet" + doc_title, "", ""])
        data.append(["", "", "", "job no.", "project leader", "scale at A3", "", "", "", "", "", ""])
        data.append(["", "", "",  projectinfo.get("Job Number"), projectinfo.get("Project Leader") ,"NTS", "", "", "", "", "", ""])
        data.append(["", "", "", "status code and description", "", "", "issue date", "classification", "revision", projectinfo.get("Naming Convention"), "", ""])
        data.append(["", "", "", s + status_description, "", "", d + "/" + m + "/" + y, "-", "-", BuildIssueSheet.document_number(history, part, project_code, add_space=True), "", ""])
        return data    


    @staticmethod
    def day_month_year_status(index, history, selected_issues=[], li_issues=[]):
        cols_to_plot = BuildIssueSheet.cols_to_plot(history=history,
                 selected_issues=selected_issues,
                 li_issues=li_issues)[index]
        d = cols_to_plot[6:8]
        m = cols_to_plot[4:6]
        y = cols_to_plot[2:4]
        s = cols_to_plot[9:]
        return d, m, y, s

    @staticmethod
    def data_table(history, part, selected_issues, li_issues, data, doc_descriptions, lookup):       
        cols = BuildIssueSheet.cols_to_plot(history=history,
                 selected_issues=selected_issues, 
                 li_issues=li_issues, part=part)
        last_col = cols[-1]
        data_tmp = data.sort_values("System Identifier Description")
        data_list = [] #this is a list of rows in the table. #list for styling output.
        sid_style = []

        uniclass_classifications = sorted(list(set([d["uniclass"] for d in doc_descriptions.values()])))
        map_uniclass_description =  {v: lookup.classification[k] for k, v in lookup.classification_uniclass.items()}
            
        for uniclass in uniclass_classifications:
            sid = map_uniclass_description[uniclass]
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

    @staticmethod
    def tablestyle(history, sid_style, data_list, headings):
        if history:
            tablestyle = highlight_last_format(headings+data_list, startrow=5, rev_position=len(DEFAULT_COLS)-1) + sid_style
        else:
            tablestyle = DEFAULTTABLESTYLE(defaultcols = len(DEFAULT_COLS)-1) + sid_style
        return tablestyle

    @staticmethod
    def distribution_table(dist_data, data_list, sid_style, history, part, selected_issues, li_issues):
        ###LET's Do the Distribution List
        cols = BuildIssueSheet.cols_to_plot(history=history,
                 selected_issues=selected_issues, 
                 li_issues=li_issues, part=part)
        
        data_list += [[""]] #blank line
        sid_style += dist_line_style(4+len(data_list))
        data_list += [["Distribution"]]
        sid_style += dist_line_style(4+len(data_list))
        distcols = ['Name']*len(DEFAULT_COLS) + [x for x in cols if not x in DEFAULT_COLS]
        for i, line in enumerate(dist_data[distcols].values.tolist()):
            sid_style.append(('SPAN', (0, 5+len(data_list)+i), (len(DEFAULT_COLS)-1, 5+len(data_list)+i)))
        data_list += dist_data[distcols].values.tolist()
        return data_list, sid_style

    @staticmethod
    def create_heading(cols_to_plot):
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
    
    
    @staticmethod
    def output_doc(document, 
                   fname, 
                   data, 
                   dist_data,
                   projectinfo, 
                   config, 
                   doc_descriptions,
                   lookup,
                   history=False, 
                   part=-1, 
                   selected_issues=[], 
                   column_widths=[100, 40, 9], 
                   li_issues=[]):

        document.filename = fname
        if not document.filename: 
            return False
        #data_list is a list of lists containing the cells of the final table.
        #sid_style is the additional styling applied to the cells over and above the standard.
        
        
        data_list, sid_style = BuildIssueSheet.data_table(history, part, selected_issues, li_issues, data, doc_descriptions, lookup)
        cols_to_plot = BuildIssueSheet.cols_to_plot(history=history,
                 selected_issues=selected_issues, 
                 li_issues=li_issues, part=part)
        headings = BuildIssueSheet.create_heading(cols_to_plot)
        data_list, sid_style = BuildIssueSheet.distribution_table(dist_data, data_list, sid_style, history, part, selected_issues, li_issues)
        titleblockdata = BuildIssueSheet.construct_title_block(history, part, selected_issues, li_issues, projectinfo, config, lookup)
        tstyle = BuildIssueSheet.tablestyle(history, sid_style, data_list, headings)
        document = issue_sheet(data_list,
                                document,
                                titleblockdata = titleblockdata,
                                headings=headings,
                                tablestyle=tstyle,
                                col_widths = column_widths[:3])  # This saves the file to pdf
        return True
    
    
    
    @staticmethod
    def print_issue_and_issue_history(data, 
                                    dist_data, 
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
                                    project_code) -> tuple[str, str]:
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
        fname = savefilename.replace(".pdf", " " + BuildIssueSheet.document_number(False, -1, project_code) + ".pdf")
        
        # output issue sheet
        if not BuildIssueSheet.output_doc(document, fname, data, dist_data, projectinfo, config, doc_descriptions, lookup, selected_issues=selected_issues, li_issues=li_issues, column_widths=column_widths): 
            return False
        else:
            filescreated.append(savefilename.replace(".pdf", " " + BuildIssueSheet.document_number(False, -1, project_code) + ".pdf"))
 
        # continue to output issue istory
        #output history
        if no_issues > max_cols_in_part: #Pagination required.
            num_parts = math.ceil(no_issues / max_cols_in_part)
            for part in range(1, num_parts+1):
                fname = savefilename.replace(".pdf", "_history " + BuildIssueSheet.document_number(True, part, project_code) + ".pdf")
                if not BuildIssueSheet.output_doc(document, 
                                                  fname, 
                                                  data, 
                                                  dist_data, 
                                                  projectinfo, 
                                                  config, 
                                                  doc_descriptions,
                                                  lookup, 
                                                  history=True, part=part, selected_issues=selected_issues, li_issues=li_issues, column_widths=column_widths): 
                    return False
                else: 
                    filescreated.append(fname)
            savefilenamehistory = filescreated[-1]
        else:
            if not BuildIssueSheet.output_doc(document, savefilenamehistory, data, dist_data, projectinfo, config, doc_descriptions, lookup, history=True, selected_issues=selected_issues, li_issues=li_issues, column_widths=column_widths): 
                return False
            else: 
                filescreated.append(savefilenamehistory)
                
        return filescreated





def gotohelp():
    webbrowser.open_new(r"mailto:helpdesk@maxfordham.com")

def new_document(projectname, office):
    ''' creates a new Max Fordham document'''
    document = MFDoc()
    document.title = projectname
    document.address = address_from_loc(office)
    document.address_compact = address_from_loc_compact(office)
    return document

def project_info():
    ''' gets the project info from the first sheet'''
    return xw.sheets['readme'].range(index_of_value("Job Number", 'readme')).options(dict, expand='table', numbers=int).value

def sid_info():
    ''' gets the System classification Codes and information from the lookup table'''
    try:
        res = xw.sheets['classification'].range(index_of_value("classification_code", 'classification')).options(pd.Series, expand='table', numbers=int).value
    except:
        res = xw.sheets['0. lookup tables'].range(index_of_value("role_code", '0. lookup tables')).options(pd.Series, expand='table', numbers=int).value
        res['uniclass_classification'] = res['classification_des']
    return res.sort_values("uniclass_classification")

def table_info(sheet, firstheader, getdict=False):
    try:
        if getdict:
            res = xw.sheets[sheet].range(index_of_value(firstheader, sheet)).options(dict, expand='table', numbers=int).value
        else:
            res = xw.sheets[sheet].range(index_of_value(firstheader, sheet)).options(pd.Series, expand='table', numbers=int).value
    except:
        res = None
    return res

def status_info():
    ''' gets the System classification Codes and information from the lookup table'''
    try:
        res = xw.sheets['status'].range(index_of_value("status_code", 'status')).options(pd.Series, expand='table', numbers=int).value
    except: #backwards compatability
        res = xw.sheets['0. lookup tables'].range(index_of_value("Code", '0. lookup tables')).options(pd.Series, expand='table', numbers=int).value
    if "status_code" not in res.columns:
        res['status_code'] = res.index
    return res

def config_filename(job_number):
    ''' return the filename of the config files.'''
    #username = os.environ['username']
    return CONFIG_DIR + "\\" + str(job_number) + ".json"

def user_config(job_number):
    ''' loads the user configuration'''
    file = config_filename(job_number)
    try:
        if os.path.isfile(file):
            with open(file, 'r') as handle:
                #config = pickle.load(handle)
                config = json.load(handle)
        else:
            config = DEFAULT_CONFIG
    except:
        logger.warning("Cannot read Job Settings. We'll carry on anyway but contact support.",
                           "Config error")

    config = verify_config(config)
    return config

def verify_config(config):
    for k in DEFAULT_CONFIG.keys():
        if k not in config:
            config[k] = DEFAULT_CONFIG[k]
    return config

def save_config(config):
    ''' save the config (which is a dict) to a file'''
    file = config_filename(config["job_number"])
    try:
        with open(file, 'w') as handle:
            #pickle.dump(config, handle)
            print(config)
            print(file)
            json.dump(config, handle, sort_keys=True, indent=4)
    except Exception as e:
        print(e)
        logger.warning("Cannot Save your User Settings. We'll carry on anyway but contact support.",
                           "Config error")

def show_file(filename):
    '''open a file in default program'''
    subprocess.Popen(filename, shell=True)

def get_distribution_data(li_issues=None):
    if index_of_value("Name", '1. Document Numbering'):
        res = xw.sheets['1. Document Numbering'].range(index_of_value("Name", '1. Document Numbering')).options(pd.Series, expand='table').value
        if type(res) is pd.core.frame.Series:
            raise ValueError("Atleast two people in distribution required.\nOnly need one? Just add a dummy one")
        res['Name'] = res.index  # TODO: this is bad
        res = res.fillna("")
        pd.options.display.float_format = '{:,.0f}'.format
        
        if li_issues is not None:  # TODO: tbc
            cols = list(res.columns)
            for i, col in enumerate(li_issues): 
                cols[i] = col
            res.columns = cols
            df = res[li_issues+["Name"]]
            res= df.loc[df.index.notnull()]
        
        return res
    raise Exception('Cannot Find Distribution Table - ensure First Column is titled "Name"')

def format_data_rows(rows):
    #rows is a list of list.
    for i, row in enumerate(rows):
        _row = row
        _row[0] = "\n".join(wrap(_row[0], 80))
        rows[i] = _row
    return rows

def get_pandas_data():
    ''' extract data from spreadsheet and convert it to a pandas dataframe'''
    if index_of_value("Document Number", '1. Document Numbering'):
        res = xw.sheets['1. Document Numbering'].range(index_of_value("Sort By Uniclass", '1. Document Numbering')).options(pd.Series, expand='table').value
        res = res.reset_index(drop=False).set_index('Document Number').rename(columns={"Sort By Uniclass": "uniclass"})
        if "Document Number" not in res.columns: #backwards compatability for spreadsheet upgrade.
            res.index.names = ['Document Number Index']
            res['Document Number'] = res.index

        if type(res) is pd.core.frame.Series:
            raise ValueError("Atleast two documents required.\nOnly need one? Just add a dummy one")
        if "Document Number" not in res.columns:
            res['Document Number'] = res.index
        res = res[res['Document Number'] != -2146826246]
        cols_to_remove = list(set(res.columns).intersection(map(str, range(0, 999))))
        cols_to_remove += [x for x in res.columns if "Column" in x or "blank" in x or "→" in x or "?" in x or "Add to " in x]
        res = res.sort_values('Document Number')
        res = res.dropna(subset=["Document Number"])
        pd.options.display.float_format = '{:,.0f}'.format
        return res.drop(cols_to_remove, axis=1) #remove column that are empty.
    raise Exception('Cannot Revision Information - Something has gone wrong contact support.')

def index_of_value(value, sheet):
    ''' look for a value in the spreadsheet '''
    for i, line in enumerate(xw.sheets[sheet].range((1, 1), (200, 200)).value):
        try: return (i+1, line.index(value)+1)
        except: pass
    return False

def add_doc(row, sheettabledict, item):
    xw.sheets['1. Document Numbering'].range(str(row)+":" + str(row)).api.Insert(xw.constants.InsertShiftDirection.xlShiftToRight)
    for i, line in enumerate(sheettabledict):
        rowcol = index_of_value(line[3], '1. Document Numbering')
        rowcol = (row, rowcol[1])
        if line[0] == "sequence":
            xw.sheets['1. Document Numbering'].range(rowcol).value = "=TEXT(" + str(item[i]) + ",\"00\")"
        else:
            xw.sheets['1. Document Numbering'].range(rowcol).value = str(item[i])