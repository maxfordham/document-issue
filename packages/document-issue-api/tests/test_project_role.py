from setup_test_client import client, clean_session, get_db_path, clear_data_func
from fastapi.encoders import jsonable_encoder
import pytest

# from document_issue.role import Project, Role
from test_project import post_project
from test_role import post_role


def post_project_role():
    post_project()
    post_role()
    return client.post("/project_role/1/1/")


@pytest.mark.usefixtures("clear_data_func")
class TestProjectRole:
    def test_post_project_role(self):
        response = post_project_role()
        assert response.status_code == 200
        assert response.json()["project"]["project_name"] == "test_project"
