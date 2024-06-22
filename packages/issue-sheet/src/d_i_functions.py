import subprocess
import os
import sys
import glob
import pickle
import json
import webbrowser
import xlwings as xw
import pandas as pd
import math as math
from itertools import product
from reportlab.lib import colors
from textwrap import wrap
from d_i_ui import warning_messagebox, info_messagebox, getsavefilename, getfoldername, MFButton, MFLabelFrame, MFLabel, MFLabelBlack, getfilename, MFHeader, MFOptionMenu, MFCheckButton, MFTk
from mf_reportlab.issuesheet_reportlab import issue_sheet
from mf_reportlab.mf_styles import MFDoc, DEFAULTTABLESTYLE, highlight_last_format
from mf_reportlab.mf_styles import p_nospace, get_titleblockimage
from mf_reportlab.mf_styles import dist_line_style, sid_line_style
from constants import address_from_loc, address_from_loc_compact, OFFICES

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



def gotohelp():
    webbrowser.open_new(r"mailto:helpdesk@maxfordham.com")

def new_document(projectname, config):
    ''' creates a new Max Fordham document'''
    document = MFDoc()
    document.title = projectname
    document.address = address_from_loc(config["office"])
    document.address_compact = address_from_loc_compact(config["office"])
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
        warning_messagebox("Cannot read Job Settings. We'll carry on anyway but contact support.",
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
        warning_messagebox("Cannot Save your User Settings. We'll carry on anyway but contact support.",
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