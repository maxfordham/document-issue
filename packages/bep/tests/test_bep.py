import os
import pathlib

import bep

fdir = pathlib.Path(__file__).parent
fpth_status_revision = fdir.joinpath("data/status_revision.csv")

def del_env_var():
    if "BEP_STATUS_REVISION" in os.environ:
        os.environ.pop("BEP_STATUS_REVISION")

def test_get_config():
    del_env_var()
    config = bep.get_config()
    assert config.STATUS_REVISION is None
    os.environ["BEP_STATUS_REVISION"] = str(fpth_status_revision)
    config = bep.get_config()
    assert config.STATUS_REVISION == fpth_status_revision

def test_get_status_revision():
    del_env_var()
    SR = bep.get_status_revision()
    assert SR is not None
    assert len(SR.root) > 0
    assert SR.root[0].status_code == "S0"
    os.environ["BEP_STATUS_REVISION"] = str(fpth_status_revision)
    SR = bep.get_status_revision()
    assert SR.root[0].status_code == "A"

def test_get_invalid_status_revision():
    os.environ["BEP_STATUS_REVISION"] = ""
    SR = bep.get_status_revision()
    assert SR.root[0].status_code == "S0"

def test_get_project_roles():
    project_roles = bep.get_project_roles()
    assert project_roles.root[0].role_title == "Director in Charge"
