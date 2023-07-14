from setup_test_client import client, clean_session, get_db_path, clear_data_func
from fastapi.encoders import jsonable_encoder
from document_issue.role import Role
import pytest

from rest_funcs import post_role


@pytest.mark.usefixtures("clear_data_func")
class TestRole:
    def test_post_role(self):
        response = post_role()
        assert response.status_code == 200
        assert response.json()["role_name"] == "test_role"

    def test_get_role(self):
        response = post_role()
        role_id = response.json()["id"]
        response = client.get(f"/role/{role_id}")
        assert response.status_code == 200
        assert response.json()["role_name"] == "test_role"

    def test_patch_role(self):
        response = post_role()
        role_id = response.json()["id"]
        response = client.patch(f"/role/{role_id}", json={"role_name": "test_role2"})
        assert response.status_code == 200
        assert response.json()["role_name"] == "test_role2"

    def test_delete_role(self):
        response = post_role()
        role_id = response.json()["id"]
        response = client.delete(f"/role/{role_id}")
        assert response.status_code == 200
        assert response.json()["role_name"] == "test_role"
        response = client.get(f"/role/{role_id}")
        assert response.status_code == 404

    def test_get_roles(self):
        response = post_role()
        role_id = response.json()["id"]
        response = client.get(f"/roles")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["id"] == role_id
        assert response
