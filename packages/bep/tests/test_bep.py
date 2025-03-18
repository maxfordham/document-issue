import os
import pathlib

import bep

fdir = pathlib.Path(__file__).parent
fpth_status_revision = fdir.joinpath("data/status_revision.csv")

def del_env_var():
    if "PROJECT_CONFIGURATION_STATUS_REVISION" in os.environ:
        os.environ.pop("PROJECT_CONFIGURATION_STATUS_REVISION")

def test_get_config():
    del_env_var()
    config = bep.get_config()
    assert config.STATUS_REVISION is None
    os.environ["PROJECT_CONFIGURATION_STATUS_REVISION"] = str(fpth_status_revision)
    config = bep.get_config()
    assert config.STATUS_REVISION == fpth_status_revision

def test_get_status_revision():
    del_env_var()
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