import pathlib

# DIR_ROOT = pathlib.Path(__file__).parent
DIR_ROOT = pathlib.Path(r"C:\engDev\git_mf\MF_Toolbox\dev\mf_xlwings\document_issue") # Set this to be Y:\drive
FPTH_ICON = str(DIR_ROOT / "mf_reportlab" / "MF_O_trans.ico")

OFFICES = ["London", "Cambridge", "Bristol", "Manchester", "Edinburgh"]

MAP_TITLEBLOCK_IMAGES = {
    l.lower(): DIR_ROOT / "mf_reportlab" / ("titleblock_" + l.lower() + ".png") for l in OFFICES
}

LONDON_ADDRESS = ["Max Fordham LLP", "42/43 Gloucester Cresecent", "Camden", "NW1 7PE", "+44 (0)207 267 5161"]
EDINBURGH_ADDRESS = ["Max Fordham LLP", "Exchange Place 3", "3 Semple Street", "Edinburgh", "EH3 8BL", "+44 (0)131 476 6001"]
BRISTOL_ADDRESS = ["Max Fordham LLP", "Queen Square House", "18-21 Queen Square", "Bristol", "BS1 4NH", "+44 (0)117 329 0874"]
MANCHESTER_ADDRESS = ["Max Fordham LLP", "Carver's Warehouse", "77 Dale Street", "Manchester", "M1 2HG", "+44 (0)161 312 8071"]
CAMBRIDGE_ADDRESS = ["Max Fordham LLP", "St Andrew's House", "59 St Andrew's Street", "Cambridge", "CB2 3BZ", "+44 (0)122 324 0155"]

LONDON_ADDRESS_COMPACT = ["Max Fordham LLP", "42/43 Gloucester Cresecent", "Camden NW1 7PE"]
EDINBURGH_ADDRESS_COMPACT = ["Max Fordham LLP", "Exchange Place 3, 3 Semple Street", "Edinburgh EH3 8BL"]
BRISTOL_ADDRESS_COMPACT = ["Max Fordham LLP", "Queen Square House, 18-21 Queen Square", "Bristol BS1 4NH"]
MANCHESTER_ADDRESS_COMPACT = ["Max Fordham LLP", "Carver's Warehouse, 77 Dale Street", "Manchester M1 2HG"]
CAMBRIDGE_ADDRESS_COMPACT = ["Max Fordham LLP", "St Andrew's House, 59 St Andrew's Street", "Cambridge CB2 3BZ"]

def address_from_loc_compact(loc):
    loc_lower = loc.lower()
    if loc_lower == "cambridge":
        return CAMBRIDGE_ADDRESS_COMPACT
    elif loc_lower =="edinburgh":
        return EDINBURGH_ADDRESS_COMPACT
    elif loc_lower == "bristol":
        return BRISTOL_ADDRESS_COMPACT
    elif loc_lower == "manchester":
        return MANCHESTER_ADDRESS_COMPACT
    else:
        return LONDON_ADDRESS_COMPACT

def address_from_loc(loc):
    loc_lower = loc.lower()
    if loc_lower == "cambridge":
        return CAMBRIDGE_ADDRESS
    elif loc_lower =="edinburgh":
        return EDINBURGH_ADDRESS
    elif loc_lower == "bristol":
        return BRISTOL_ADDRESS
    elif loc_lower == "manchester":
        return MANCHESTER_ADDRESS
    else:
        return LONDON_ADDRESS
        

import os
# DIR = r"Y:\git_projects\MF_Toolbox\dev\mf_modules"
DIR = r"C:\engDev\MF_Toolbox\dev\mf_modules"

def mf_modules_dir():
    ''' use this when referencing files.'''

    try:
        pythonpath = os.environ['PYTHONPATH'].split(";")
        for i in pythonpath:
            if "mf_toolbox" in i.lower():
                return i + r'\mf_modules'
        _MF_ROOT = os.environ['mf_root']
        return os.path.join(_MF_ROOT,r'mf_modules') #fallback
    except:
        return os.path.join(DIR)