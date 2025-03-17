import bep
import os
import importlib
import pathlib


fdir = pathlib.Path(__file__).parent
fpth_status_revision = fdir.joinpath("data/status_revision.csv")


def test_get_config():
    config = bep.get_config()
    assert config.STATUS_REVISION is None
    os.environ["PROJECT_CONFIGURATION_STATUS_REVISION"] = str(fpth_status_revision)
    config = bep.get_config()
    assert config.STATUS_REVISION == fpth_status_revision

def test_get_status_revision():
    SR = bep.get_status_revision()
    # ST = bep.get_default_status_revision_table()
    assert SR is not None
    assert len(SR.root) > 0
    assert SR.root[0].status_code == "S0"
    os.environ["PROJECT_CONFIGURATION_STATUS_REVISION"] = str(fpth_status_revision)
    SR = bep.get_status_revision()
    assert SR.root[0].status_code == "A"

def test_get_invalid_status_revision():
    os.environ["PROJECT_CONFIGURATION_STATUS_REVISION"] = ""
    SR = bep.get_status_revision()
    assert SR.root[0].status_code == "S0"