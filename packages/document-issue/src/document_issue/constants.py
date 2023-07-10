import pathlib

COL_WIDTH = 100

# dev
DIR_TESTS = pathlib.Path(__file__).parent
DIR_MODULE = DIR_TESTS.parent

PATH_MFOM = pathlib.Path(__file__).parent
DIR_TEMPLATES = PATH_MFOM / "templates"
PATH_REFERENCE_DOCX = DIR_TEMPLATES / "default_refdocx.docx"
NAME_MD_DOCISSUE_TEMPLATE = "docissue.md.jinja"
NAME_MD_DISCLAIMER_TEMPLATE = "disclaimer.md.jinja"
PATH_REL_IMG = pathlib.Path("images")

FNM_JOB_DATA_INI = "Jobdata.ini"
FNM_EXAMPLE_JOB = "J5001"
DEFAULT_PROJECT_NUMBER = 3870


if __name__ == "__main__":
    if __debug__:
        print("loaded")
