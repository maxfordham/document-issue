"""get default status revision table."""
from .custom import SETTINGS, BaseSettings
from .default import get_default_project_roles, get_default_status_revision_table
from .models import ProjectRoleTable, StatusRevisionTable, read_csv_records


def get_config() -> BaseSettings:
    """Get the configuration settings."""
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

def get_project_roles()-> ProjectRoleTable:
    """Get project roles table from default or custom location."""
    return get_default_project_roles()
