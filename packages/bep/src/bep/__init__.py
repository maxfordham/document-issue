"""get default status revision table."""
from .custom import SETTINGS
from .default import get_default_status_revision_table
from .models import StatusRevisionTable, read_csv_records
import pathlib

def get_config():
    SETTINGS.__init__()
    return SETTINGS

def get_status_revision() -> StatusRevisionTable:
    """Get the status revision table from default or custom location."""
    SETTINGS.__init__()
    if SETTINGS.STATUS_REVISION is None: 
        return get_default_status_revision_table()
    
    if not SETTINGS.STATUS_REVISION.is_file():  # TODO: update to allow for retrieval from URL etc.
        return get_default_status_revision_table()

    return read_csv_records(SETTINGS.STATUS_REVISION, StatusRevisionTable)


