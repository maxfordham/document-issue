from setup_test_client import client, clean_session, get_db_path
from fastapi.encoders import jsonable_encoder
from document_issue.project import Role


def post_role(role: Role):
    _ = jsonable_encoder(role)
    return client.post("/role/", json=_)


class TestRole:
    def test_post_role(self):
        role = Role()
        response = post_role(role)
        assert response.status_code == 200
