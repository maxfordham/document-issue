from setup_test_client import client, get_db_path  # , clear_data_func, clean_session
from fastapi.encoders import jsonable_encoder
import pytest

# from document_issue.role import Project, Role
from setup_test_client import post_project_role_with_person_and_document_role


# @pytest.mark.usefixtures("clear_data_func")
# class TestDocumentRole:
#     def test_post_document_role(self):
#         response = post_project_role_with_person_and_document_role()

#         assert response.status_code == 200
#         r = response.json()
#         assert r["role_id"] == 1

#     def test_get_document_roles(self):
#         post_project_role_with_person_and_document_role()
#         response = client.get("/document_roles/1")
#         assert response.status_code == 200
#         r = response.json()
#         assert r[0]["role_id"] == 1

#     def test_delete_document_role(self):
#         post_project_role_with_person_and_document_role()
#         response = client.delete("/document_role/1/1")
#         assert response.status_code == 200
#         r = response.json()
#         assert r["role_id"] == 1
