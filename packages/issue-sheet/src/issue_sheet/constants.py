import pathlib

MAX_COLS_IN_PART = 30
CONFIG_DIR = r"J:\J4321\Data\document_issue\config"
CONFIG_DIR = str(pathlib.Path(__file__).parent.parent.parent / "tests" / "config")
DEFAULT_CONFIG = {
    "job_number": "4321",
    "office": "Cambridge",  # edinburgh; bristol; manchester; cambridge; london;
    "open_on_save": "False",
    "check_on_save": "True",
    "col_widths": "100,40,9",
    "max_cols_in_part": MAX_COLS_IN_PART,
    "users": [],
    "timestamps": [],
    "filepath": "",
}
