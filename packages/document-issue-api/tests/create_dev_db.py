import pathlib
import shutil

import pytest
from setup_test_client import (
    client,
    post_document,
    post_issue,
    post_person,
    post_project,
    post_role,
)


@pytest.fixture
def post_data_then_delete():
    post_person()
    post_project()
    post_role()
    post_document()
    client.post("/project_role/1/1/", params={"person_id": 1})
    client.post("/document_role/1/1")
    post_issue()
    yield
    client.delete("/person/1/")
    client.delete("/project/1/")
    client.delete("/role/1/")
    client.delete("/document/1/")
    client.delete("/project_role/1/1/")
    client.delete("/document_role/1/1/")
    client.delete("/issue/1/")


def test_copy_testdb_to_appdb(post_data_then_delete):
    """Setup a test database and copy it to the app database"""
    r = post_data_then_delete
    p_test = pathlib.Path(__file__).parent / "test.db"
    p_app = pathlib.Path(__file__).parents[1] / "src" / "document_issue_api" / "app.db"

    p_app.unlink(missing_ok=True)
    assert not p_app.is_file()
    shutil.copyfile(p_test, p_app)
    assert p_app.is_file()
