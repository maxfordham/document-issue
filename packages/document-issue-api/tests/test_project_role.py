import pytest
from setup_test_client import client, post_project, post_role, post_person


def post_project_role():
    post_project()
    post_role()
    return client.post("/project_role/1/1/")


def post_project_role_with_person():
    post_person()
    post_project()
    post_role()
    return client.post("/project_role/1/1/", params={"person_id": 1})


@pytest.fixture
def post_project_role_then_delete():
    r = post_project_role_with_person()
    yield r
    client.delete("/project_role/1/1/")
    client.delete("/person/1/")
    client.delete("/project/1/")
    client.delete("/role/1/")


def test_post_project_role(post_project_role_then_delete):
    response = post_project_role_then_delete
    assert response.status_code == 200
    r = response.json()
    assert isinstance(r["project"]["project_name"], str)


def test_get_project_role(post_project_role_then_delete):
    _ = post_project_role_then_delete
    response = client.get("/project_role/1/1/")
    assert response.status_code == 405


def test_get_project_roles(post_project_role_then_delete):
    r = post_project_role_then_delete
    response = client.get("/project_roles/1/")
    assert response.status_code == 200
    r = response.json()
    assert isinstance(r["project_roles"], list)


def test_delete_project_role(post_project_role_then_delete):
    r = post_project_role_then_delete
    response = client.delete("/project_role/1/1/")
    assert response.status_code == 200
    client.post("/project_role/1/1/")
