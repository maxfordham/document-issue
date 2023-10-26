import pathlib

FDIR_PACKAGE_ROOT = pathlib.Path(__file__).parents[2]
FDIR_PACKAGE = pathlib.Path(__file__).parent
FDIR_TEMPLATES = FDIR_PACKAGE / "templates"
FDIR_MEDIA = FDIR_PACKAGE / "media"
NAME_MD_DOCISSUE_TEMPLATE = "docissue.md.jinja"
