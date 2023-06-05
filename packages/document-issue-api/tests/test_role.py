from setup_test_client import client, clean_session, get_db_path, clear_data_func
from fastapi.encoders import jsonable_encoder
from document_issue.role import Role
import pytest


def post_role():
    role = Role(role_name="test_role", role_description="test_description")
    _ = jsonable_encoder(role)
    return client.post("/role/", json=_)


@pytest.mark.usefixtures("clear_data_func")
class TestRole:
    def test_post_role(self):
        response = post_role()
        assert response.status_code == 200
        assert response.json()["role_name"] == "test_role"
