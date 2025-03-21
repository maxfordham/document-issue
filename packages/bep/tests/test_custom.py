import os
import pathlib

fdir = pathlib.Path(__file__).parent
fpth_status_revision = fdir.joinpath("data/status_revision.csv")



def test_custom_status_revision():
    import bep
    os.environ["BEP_STATUS_REVISION"] = str(fpth_status_revision)
    status_revision = bep.get_status_revision()
    fpth_status_revision == status_revision

def test_custom_roles():
    import bep
    os.environ["BEP_PROJECT_ROLES"] = "bep.model._test_get_project_roles_table"
    roles = bep.get_project_roles()
    assert roles.root[0].role_title == "Director in Charge"
