from setup_test_client import client, get_db_path  # clean_session, clear_data_func
from fastapi.encoders import jsonable_encoder
from document_issue.role import Role
import pytest

from setup_test_client import post_role, delete_role


@pytest.fixture
def post_role_then_delete():
    role = post_role()
    assert role.status_code == 200
    assert role.json()["role_name"] == "test_role"
    yield role
    id_ = role.json()["id"]
    delete_role(id_)
    assert delete_role(id_).status_code == 404
    assert client.get(f"/role/{id_}").status_code == 404


def test_post_role(post_role_then_delete):
    response = post_role_then_delete
    assert response.status_code == 200
    assert response.json()["role_name"] == "test_role"


def test_get_role(post_role_then_delete):
    response = post_role_then_delete
    role_id = response.json()["id"]
    response = client.get(f"/role/{role_id}")
    assert response.status_code == 200
    assert response.json()["role_name"] == "test_role"


def test_get_roles(post_role_then_delete):
    response = post_role_then_delete
    response = client.get(f"/roles/")
    assert response.status_code == 200
    assert response.json()[0]["role_name"] == "test_role"


def test_patch_role(post_role_then_delete):
    response = post_role_then_delete
    role_id = response.json()["id"]
    response = client.patch(f"/role/{role_id}", json={"role_name": "test_role2"})
    assert response.status_code == 200
    assert response.json()["role_name"] == "test_role2"


def test_delete_role(post_role_then_delete):
    response = post_role_then_delete
    role_id = response.json()["id"]
    response = client.delete(f"/role/{role_id}")
    assert response.status_code == 200
    assert response.json()["role_name"] == "test_role"
    response = client.get(f"/role/{role_id}")
    assert response.status_code == 404
    post_role()  # do it can be deleted again
