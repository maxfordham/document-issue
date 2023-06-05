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

    def test_get_project_role(self):
        response = post_project_role()
        assert response.status_code == 200
        assert response.json()["project"]["project_name"] == "test_project"

        # response = client.get("/project_role/1/1/")
        # assert response.status_code == 200
        # assert response.json()["project"]["project_name"] == "test_project"

        post_role(role_name="test_role2")
        client.post("/project_role/1/1/")
        response = client.post("/project_role/1/2/")
        response = client.get("/project_roles/1/")
        assert response.status_code == 200
        assert response.json()["roles"][0]["role_name"] == "test_role"
        assert response.json()["roles"][1]["role_name"] == "test_role2"

    def test_delete_project_role(self):
        # response =
        # assert response.status_code == 200
        # assert response.json()["project"]["project_name"] == "test_project"
        post_project_role()

        response = client.delete("/project_role/1/1/")
        assert response.status_code == 200
        assert response.json()["project"]["project_name"] == "test_project"

        response = client.get("/project_roles/1/")
        assert response.status_code == 200
        assert response.json()["roles"] == []
