import os
import pathlib

fdir = pathlib.Path(__file__).parent
fpth_status_revision = fdir.joinpath("data/status_revision.csv")

os.environ["PROJECT_CONFIGURATION_STATUS_REVISION"] = str(fpth_status_revision)

def test_custom():

    import bep
    STATUS_REVISION = bep.get_status_revision()
    fpth_status_revision == STATUS_REVISION
