import pathlib


# dev
DIR_TESTS = pathlib.Path(__file__).parent
DIR_MODULE = DIR_TESTS.parent

PATH_MFOM = pathlib.Path(__file__).parent
DIR_TEMPLATES = PATH_MFOM / "templates"
PATH_REFERENCE_DOCX = DIR_TEMPLATES / "default_refdocx.docx"
NAME_MD_HEADER_TEMPLATE = "docheader.md.jinja"
NAME_MD_DISCLAIMER_TEMPLATE = "disclaimer.md.jinja"
PATH_REL_IMG = pathlib.Path("images")

FNM_JOB_DATA_INI = "Jobdata.ini"
FNM_EXAMPLE_JOB = "J5001"

# documentinfo ------------------------------
#  update this with WebApp data
ROLES = (
    "Design Lead",
    "Project Engineer",
    "Engineer",
    "Project Coordinator",
    "Project Administrator",
    "Building Performance Modeller",
    "Passivhaus Engineer",
    "Sustainability Consultant",
)


if __name__ == "__main__":
    if __debug__:
        print("loaded")
