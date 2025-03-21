from importlib.resources import files
import mysql.connector
from .models import ProjectRoleTable, StatusRevisionTable, read_csv_records
import logging

logger = logging.getLogger(__name__)

DIR_DEFAULT = files("bep.data")
PTH_STATUS_REVISION_TABLE = DIR_DEFAULT.joinpath("status_revision.csv")
PTH_PROJECT_ROLES = DIR_DEFAULT.joinpath("project_roles.csv")


def get_default_status_revision_table() -> StatusRevisionTable:
    """Get the default status revision table."""
    return read_csv_records(PTH_STATUS_REVISION_TABLE, StatusRevisionTable)


def get_default_project_roles()->ProjectRoleTable:
    """Get the default project roles. Try to read from database, if not available, read from csv."""
    return read_csv_records(PTH_PROJECT_ROLES, ProjectRoleTable)
