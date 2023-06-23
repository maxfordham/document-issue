import pathlib

DIR_PACKAGE = pathlib.Path(__file__).parent
DIR_TEMPLATES = DIR_PACKAGE / "templates"
PATH_REFERENCE_DOCX = DIR_TEMPLATES / "default_refdocx.docx"
NAME_MD_DOCISSUE_TEMPLATE = "docissue.md.jinja"
NAME_MD_DISCLAIMER_TEMPLATE = "disclaimer.md.jinja"
PATH_REL_IMG = pathlib.Path("images")
