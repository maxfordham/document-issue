import pytest
from setup_test_client import client, post_project


def delete_project(project_id=1):
    return client.delete(f"/project/{project_id}")


@pytest.fixture
def post_project_then_delete():
    r = post_project()
    assert r.status_code == 200
    assert r.json()["project_name"] == "test_project"
    yield r
    id_ = r.json()["id"]
    r1 = delete_project(id_)
    assert r1.status_code == 200
    assert client.get(f"/project/{id_}").status_code == 404


def test_post_project(post_project_then_delete):
    response = post_project_then_delete
    assert response.status_code == 200
    assert isinstance(response.json()["project_name"], str)


def test_get_project(post_project_then_delete):
    response = post_project_then_delete
    project_id = response.json()["id"]
    response = client.get(f"/project/{project_id}")
    assert response.status_code == 200
    assert isinstance(response.json()["project_name"], str)


def test_get_projects(post_project_then_delete):
    _ = post_project_then_delete
    response = client.get("/project/")
    assert response.status_code == 200
    r = response.json()
    assert isinstance(r, list)
    assert isinstance(r[0]["project_name"], str)


def test_patch_project(post_project_then_delete):
    response = post_project_then_delete
    project_id = response.json()["id"]
    response = client.patch(f"/project/{project_id}", json={"project_name": "test_project2"})
    assert response.status_code == 200
    assert response.json()["project_name"] == "test_project2"


def test_delete_project():
    response = post_project()
    project_id = response.json()["id"]
    response = client.delete(f"/project/{project_id}")
    assert response.status_code == 200
    assert response.json()["project_name"] == "test_project"
    response = client.get(f"/project/{project_id}")
    assert response.status_code == 404
