from setup_test_client import client, clean_session, get_db_path, clear_data_func
from fastapi.encoders import jsonable_encoder
import pytest
from document_issue.document import DocumentBase
from test_project import post_project
from rest_funcs import post_issue, post_document, post_project_role_with_person_and_document_role


@pytest.mark.usefixtures("clear_data_func")
class TestDocument:
    def test_post_document(self):
        post_project()
        response = post_document()
        assert response.status_code == 200
        assert response.json()["document_code"] == "06667-MXF-XX-XX-SH-M-20003"

    def test_get_document(self):
        post_project()
        post_document()
        response = client.get("/document/1/")
        assert response.status_code == 200
        assert response.json()["document_code"] == "06667-MXF-XX-XX-SH-M-20003"

    def test_get_document_issue(self):
        post_project_role_with_person_and_document_role()
        post_issue()
        response = client.get("/document_issue/1/")
        assert response.status_code == 200
        r = response.json()
        assert r["document_code"] == "06667-MXF-XX-XX-SH-M-20003"
        assert r["project"]["project_number"] == 1234
        assert r["issue"][0]["revision"] == "P01"
        assert r["document_role"][0]["role"]["role_name"] == "test_role"

    def test_get_documents(self):
        post_project()
        post_document()
        response = client.get("/documents/")
        assert response.status_code == 200
        assert response.json()[0]["document_code"] == "06667-MXF-XX-XX-SH-M-20003"

    def test_patch_document(self):
        post_project()
        doc = post_document().json()
        doc["document_code"] = "06667-MXF-XX-XX-SH-M-20004"
        response = client.patch("/document/1/", json=doc)
        assert response.status_code == 200
        assert response.json()["document_code"] == "06667-MXF-XX-XX-SH-M-20004"
