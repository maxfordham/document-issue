from .models import StatusRevisionTable, read_csv_records
from importlib.resources import files

DIR_DEFAULT = files("bep.data")
PTH_STATUS_REVISION_TABLE = DIR_DEFAULT.joinpath("status_revision.csv")

def get_default_status_revision_table() -> StatusRevisionTable:
    """Get the default status revision table."""
    return read_csv_records(PTH_STATUS_REVISION_TABLE, StatusRevisionTable)