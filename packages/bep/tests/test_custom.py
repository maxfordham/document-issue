
import os
import importlib
import pathlib


fdir = pathlib.Path(__file__).parent
fpth_status_revision = fdir.joinpath("data/status_revision.csv")
import os
os.environ["PROJECT_CONFIGURATION_STATUS_REVISION"] = str(fpth_status_revision)

def test_custom():
    
    import project_configuration
    project_configuration.STATUS_REVISION
    project_configuration.SETTINGS.STATUS_REVISION == fpth_status_revision
