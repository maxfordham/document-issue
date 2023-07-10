from enum import Enum

roles = """Director in Charge
Client Relationship Management (CRM) Lead
Management Lead
Commercial Lead
Design Strategy Lead
Health and Safety Lead
Project Coordinator
Project Administrator
Strategy Reviewer
Technical Reviewer
Project Engineer
Lead Electrical Engineer
Lead Mechanical Engineer
Systems Engineer
Site Engineer
BIM Strategy Advisor
Digital Design Engineer
Responsible Building Performance Modeller
Building Performance Modeller
Lead Sustainability Consultant
Sustainability Consultant
Lead Acoustician
Specialist Building Physics Engineer
Specialist Lighting Designer
Passivhaus Principal
Passivhaus Project Designer
Passivhaus Designer
""".splitlines()

RoleEnum = Enum(
    "RoleEnum",
    roles,
)

PaperSizeEnum = Enum(
    "PaperSizeEnum",
    [
        "n/a",  # Not a drawing, 3D model for example
        "A5",  # probs never used...
        "A4",  # Sketched only, not normally used for drawings
        "A3",  # Sketch drawings, small schematics, details
        "A2",  # Not a common paper size, avoid
        "A1",  # Layouts, often at 1:100 scale
        "A0",  # Layouts, common to use at 1:50 scale to avoid an excessive number of drawing tiles
    ],
)

ScalesEnum = Enum(
    "ScalesEnum",
    [
        "nts",
        "1:1",
        "1:2",
        "1:5",
        "1:10",
        "1:20",
        "1:25",
        "1:50",
        "1:100",
        "1:200",
        "1:250",
        "1:500",
        "1:1000",
        "1:1250",
    ],
)


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
    AM = "Ametch"


class IssueFormatEnum(Enum):
    """maps IssueFormat codes to string description"""

    cde = "Uploaded to the project common data environment"
    ea = "Sent as Email attachment"
    el = "Sent as Email with a link to file download"
    p = "paper - full size"
    r = "paper - reduced size"


# class IssueFormatEnum(str, Enum):
#     """in what form was the issue delivered"""

#     cde = "cde"
#     ea = "ea"
#     el = "el"
#     p = "p"
#     r = "r"
