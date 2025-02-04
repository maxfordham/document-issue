import pathlib

MAX_COLS_IN_PART = 30


def get_config_dir(try_debug=True):
    if (
        pathlib.Path(
            r"C:\engDev\git_mf\document-issue\packages\document-issue-xl\tests\config",
        ).exists()
        and try_debug
    ):
        return (
            r"C:\engDev\git_mf\document-issue\packages\document-issue-xl\tests\config"
        )
    return r"J:\J4321\Data\document_issue\config"


CONFIG_DIR = get_config_dir()
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
TITLETEXT = "Check and create issue sheets.\n v0.2.0 - May19"
DEFAULT_COLS = [
    "Document Title",
    "Document Number",
    "docSource",
    "Scale",
    "Size",
    "Current Rev",
]
