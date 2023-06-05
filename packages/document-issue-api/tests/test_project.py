from setup_test_client import client, clean_session, get_db_path, clear_data_func
from fastapi.encoders import jsonable_encoder
import pytest
from document_issue.project import ProjectBase, Project


def post_project():
    project = ProjectBase(project_name="test_project", project_number=1234)
    _ = jsonable_encoder(project)
    return client.post("/project/", json=_)


@pytest.mark.usefixtures("clear_data_func")
class TestProject:
    def test_post_project(self):
        response = post_project()
        assert response.status_code == 200

    def test_get_project(self):
        post_project()
        response = client.get("/project/1")
        assert response.status_code == 200
        assert response.json()["project_name"] == "test_project"
        assert response.json()["project_number"] == 1234

        response = client.get("/project/")
        assert response.status_code == 200
        assert response.json()[0]["project_name"] == "test_project"

    def test_patch_project(self):
        post_project()
        response = client.patch("/project/1/", json={"project_name": "new_project"})
        assert response.status_code == 200
        assert response.json()["project_name"] == "new_project"

    def test_delete_project(self):
        post_project()
        response = client.delete("/project/1")
        assert response.status_code == 200
        assert response.json()["project_name"] == "test_project"
        assert response.json()["project_number"] == 1234

        response = client.get("/project/1")
        assert response.status_code == 204
        print("done")
