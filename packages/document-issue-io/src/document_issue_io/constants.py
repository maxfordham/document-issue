import pathlib
from importlib.resources import files

from reportlab.lib import colors

# ^ REF: https://setuptools.pypa.io/en/latest/userguide/datafiles.html#accessing-data-files-at-runtime

NAME_MD_DOCISSUE_TEMPLATE = "docissue.md.jinja"
OFFICES = ["London", "Cambridge", "Bristol", "Manchester", "Edinburgh"]

DIR_MEDIA = files("document_issue_io.media")
DIR_FONTS = files("document_issue_io.fonts")
DIR_TEMPLATES = pathlib.Path(__file__).parent / "templates"  # pathlib dir required...
LOGO = DIR_FONTS.joinpath("mf_medium.jpg")
FPTH_MF_CIRCLE_IMG = DIR_MEDIA.joinpath("mf-circle.png")
FPTH_ICON = DIR_MEDIA.joinpath("mf-icon.ico")

FONTS = {
    "Calibri": DIR_FONTS.joinpath("calibri.ttf"),
    "Calibri-Bold": DIR_FONTS.joinpath("calibrib.ttf"),
    "Calibri-Light-Italics": DIR_FONTS.joinpath("calibrili.ttf"),
    "Calibri-Italics": DIR_FONTS.joinpath("calibrii.ttf"),
    "Calibri-Light": DIR_FONTS.joinpath("calibril.ttf"),
    "Calibri-Bold-Italics": DIR_FONTS.joinpath("calibrib.ttf"),
}


MAP_TITLEBLOCK_IMAGES = {l.lower(): DIR_MEDIA.joinpath("titleblock_" + l.lower() + ".png") for l in OFFICES}


LONDON_ADDRESS = [
    "Max Fordham LLP",
    "42/43 Gloucester Cresecent",
    "Camden",
    "NW1 7PE",
    "+44 (0)207 267 5161",
]
EDINBURGH_ADDRESS = [
    "Max Fordham LLP",
    "Exchange Place 3",
    "3 Semple Street",
    "Edinburgh",
    "EH3 8BL",
    "+44 (0)131 476 6001",
]
BRISTOL_ADDRESS = [
    "Max Fordham LLP",
    "Queen Square House",
    "18-21 Queen Square",
    "Bristol",
    "BS1 4NH",
    "+44 (0)117 329 0874",
]
MANCHESTER_ADDRESS = [
    "Max Fordham LLP",
    "Carver's Warehouse",
    "77 Dale Street",
    "Manchester",
    "M1 2HG",
    "+44 (0)161 312 8071",
]
CAMBRIDGE_ADDRESS = [
    "Max Fordham LLP",
    "St Andrew's House",
    "59 St Andrew's Street",
    "Cambridge",
    "CB2 3BZ",
    "+44 (0)122 324 0155",
]

LONDON_ADDRESS_COMPACT = [
    "Max Fordham LLP",
    "42/43 Gloucester Cresecent",
    "Camden NW1 7PE",
]
EDINBURGH_ADDRESS_COMPACT = [
    "Max Fordham LLP",
    "Exchange Place 3, 3 Semple Street",
    "Edinburgh EH3 8BL",
]
BRISTOL_ADDRESS_COMPACT = [
    "Max Fordham LLP",
    "Queen Square House, 18-21 Queen Square",
    "Bristol BS1 4NH",
]
MANCHESTER_ADDRESS_COMPACT = [
    "Max Fordham LLP",
    "Carver's Warehouse, 77 Dale Street",
    "Manchester M1 2HG",
]
CAMBRIDGE_ADDRESS_COMPACT = [
    "Max Fordham LLP",
    "St Andrew's House, 59 St Andrew's Street",
    "Cambridge CB2 3BZ",
]

START_ROW = 35  # Default
START_COL = 1  # B
MAX_COLS_IN_PART = 30

DEFAULT_COLS = [
    "Document Title",
    "Document Number",
    "docSource",
    "Scale",
    "Size",
    "Current Rev",
]
DEFAULT_TITLES = [
    "Document Title",
    "Document Number",
    "Type",
    "Scale",
    "Size",
    "Rev",
    "Dated Issue Revisions",
]

HIGHLIGHT_COLOUR = colors.Color(168 / 255, 231 / 255, 255 / 255, alpha=1.0)

SHEETTABLEDICT = [  # sheet, first header, dict?, tableheader, header in revit export
    ["project", "project_code", True, "Project Name", None],
    ["originator", "originator_code", True, "Originator Description", None],
    ["volume", "volume_code", True, "Volume Name", "03. Volume"],
    ["level", "level_code", True, "Level Description", "04. Level"],
    ["infoType", "infoType_code", True, "Information Type Description", None],
    [
        "classification",
        "classification_code",
        False,
        "System Identifier Description",
        "07. Classification",
    ],
    ["drwgType", "drwgType_code", True, "X Sequence Number", "08. Number"],
    ["sequence", "sequence_code", False, "YZ Sequence Number", "08. Number"],
]


def address_from_loc_compact(loc):
    loc_lower = loc.lower()
    if loc_lower == "cambridge":
        return CAMBRIDGE_ADDRESS_COMPACT
    if loc_lower == "edinburgh":
        return EDINBURGH_ADDRESS_COMPACT
    if loc_lower == "bristol":
        return BRISTOL_ADDRESS_COMPACT
    if loc_lower == "manchester":
        return MANCHESTER_ADDRESS_COMPACT
    return LONDON_ADDRESS_COMPACT


def address_from_loc(loc):
    loc_lower = loc.lower()
    if loc_lower == "cambridge":
        return CAMBRIDGE_ADDRESS
    if loc_lower == "edinburgh":
        return EDINBURGH_ADDRESS
    if loc_lower == "bristol":
        return BRISTOL_ADDRESS
    if loc_lower == "manchester":
        return MANCHESTER_ADDRESS
    return LONDON_ADDRESS
