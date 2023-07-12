from setup_test_client import client, clean_session, get_db_path, clear_data_func
from fastapi.encoders import jsonable_encoder
import pytest

# from document_issue.role import Project, Role
from test_project import post_project
from test_role import post_role
from test_person import post_person


def post_project_role():
    post_project()
    post_role()
    return client.post("/project_role/1/1/")


def post_project_role_with_person():
    post_person()
    post_project()
    post_role()
    return client.post("/project_role/1/1/", params={"person_id": 1})


@pytest.mark.usefixtures("clear_data_func")
class TestProjectRole:
    def test_post_project_role(self):
        response = post_project_role()
        assert response.status_code == 200
        assert response.json()["project"]["project_name"] == "test_project"

    def test_post_project_role_with_person(self):
        response = post_project_role_with_person()
        assert response.status_code == 200
        assert response.json()["person"]["initials"] == "JG"

    def test_get_project_role(self):
        response = post_project_role()
        assert response.status_code == 200
        assert response.json()["project"]["project_name"] == "test_project"

        post_role(role_name="test_role2")
        client.post("/project_role/1/1/")
        response = client.post("/project_role/1/2/")

    def test_get_project_roles(self):
        post_project_role_with_person()
        role = post_role(role_name="test_role2").json()
        role_id = role["id"]
        project_role = client.post("/project_role/1/2/", params={"person_id": 1}).json()

        response = client.get("/project_roles/1/")
        r = response.json()
        assert response.status_code == 200
        assert r["project_roles"][0]["role"]["role_name"] == "test_role"
        assert r["project_roles"][1]["role"]["role_name"] == "test_role2"

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
        assert response.json()["project_roles"] == []
