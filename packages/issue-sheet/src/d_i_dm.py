import xlwings as xw
import pandas as pd

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

def table_info(sheet, firstheader, getdict=False):
    try:
        if getdict:
            res = xw.sheets[sheet].range(index_of_value(firstheader, sheet)).options(dict, expand='table', numbers=int).value
        else:
            res = xw.sheets[sheet].range(index_of_value(firstheader, sheet)).options(expand='table', numbers=int).value
    except:
        res = None
    return res

def index_of_value(value, sheet):
    ''' look for a value in the spreadsheet '''
    for i, line in enumerate(xw.sheets[sheet].range((1, 1), (200, 200)).value):
        try: return (i+1, line.index(value)+1)
        except: pass
    return False

class DocMan():
    def __init__(self, fname):
        self.fname = fname
        xw.Book(self.fname).set_mock_caller()
        self.sheettabledict = SHEETTABLEDICT
        self.data = {}
        try:
            for l in self.sheettabledict:
                self.data[l[0]] = table_info(l[0], l[1], l[2])
            self.listboxes = []
        except:
            print("ERROR")
    