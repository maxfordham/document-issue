"""Enums for document issue module. Most defined in `bep` package."""
import csv
from enum import Enum

from bep import get_status_revision


class RoleEnum(Enum):
    director = "Director in Charge"
    lead_crm = "Client Relationship Management (CRM) Lead"
    lead_management = "Management Lead"
    lead_commercial = "Commercial Lead"
    lead_design = "Design Strategy Lead"
    lead_mechanical = "Lead Mechanical Engineer"
    lead_electrical = "Lead Electrical Engineer"
    lead_h_and_s = "Health and Safety Lead"
    lead_sustainability = "Lead Sustainability Consultant"
    lead_bpm = "Lead Building Performance Modeller"
    lead_acoustics = "Lead Acoustician"
    lead_passivhaus = "Lead Passivhaus"
    project_engineer = "Project Engineer"
    proj_coordinator = "Project Coordinator"
    proj_admin = "Project Administrator"
    rev_strategy = "Strategy Reviewer"
    rev_technical = "Technical Reviewer"
    eng_bpm = "Building Performance Modeller"
    eng_systems = "Systems Engineer"
    eng_site = "Site Engineer"
    eng_digital = "Digital Design Engineer"
    eng_acoustics = "Acoustician"
    eng_passivhaus = "Passivhaus Engineer"
    con_sustainability = "Sustainability Consultant"
    con_bim = "BIM Strategy Advisor"


# TODO: map role descriptions ?


class PaperSizeEnum(Enum):
    na = "n/a"  # Not a drawing, 3D model for example
    A5 = "A5"  # probs never used...
    A4 = "A4"  # Sketched only, not normally used for drawings
    A3 = "A3"  # Sketch drawings, small schematics, details
    A2 = "A2"  # Not a common paper size, avoid
    A1 = "A1"  # Layouts, often at 1:100 scale
    A0 = "A0"  # Layouts, common to use at 1:50 scale to avoid an excessive number of drawing tiles


class ScalesEnum(Enum):
    nts = "nts"
    _1_1 = "1:1"
    _1_2 = "1:2"
    _1_5 = "1:5"
    _1_10 = "1:10"
    _1_20 = "1:20"
    _1_25 = "1:25"
    _1_50 = "1:50"
    _1_100 = "1:100"
    _1_200 = "1:200"
    _1_250 = "1:250"
    _1_500 = "1:500"
    _1_1000 = "1:1000"
    _1_1250 = "1:1250"


class DocSource(Enum):
    A = "AutoCAD"
    R18 = "Revit18"
    R19 = "Revit19"
    R20 = "Revit20"
    R21 = "Revit21"
    R22 = "Revit22"
    R23 = "Revit23"
    PDF = "Bluebeam"
    PSD = "Photoshop"
    PNG = "Image"
    WD = "Word"
    EXL = "Excel"
    AM = "Amtech"
    DS = "DigitalSchedulesApp"


class IssueFormatEnum(Enum):
    """maps IssueFormat codes to string description."""

    cde = "Uploaded to the project common data environment"
    ea = "Sent as Email attachment"
    el = "Sent as Email with a link to file download"
    p = "paper - full size"
    r = "paper - reduced size"



MAP_STATUS = get_status_revision().map_status

StatusRevisionEnum = Enum("StatusRevisionEnum", MAP_STATUS)
