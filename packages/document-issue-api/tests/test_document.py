from setup_test_client import client, clean_session, get_db_path, clear_data_func
from fastapi.encoders import jsonable_encoder
import pytest
from document_issue.document import DocumentBase
from test_project import post_project

from document_issue_api.document.schemas import DocumentBasePost


def post_document(document: DocumentBasePost):
    _ = jsonable_encoder(document)
    return client.post(f"/document/", json=_)


@pytest.mark.usefixtures("clear_data_func")
class TestDocument:
    def test_post_document(self):
        post_project()
        document = DocumentBasePost(project_id=1)
        response = post_document(document)
        assert response.status_code == 200
        assert response.json()["document_code"] == "06667-MXF-XX-XX-SH-M-20003"

    def test_get_document(self):
        post_project()
        document = DocumentBasePost(project_id=1)
        post_document(document)
        response = client.get("/document/1/")
        assert response.status_code == 200
        assert response.json()["document_code"] == "06667-MXF-XX-XX-SH-M-20003"

    def test_get_document_issue(self):
        post_project()
        document = DocumentBasePost(project_id=1)
        post_document(document)
        response = client.get("/document_issue/1/")
        assert response.status_code == 200
        r = response.json()
        assert r["document_code"] == "06667-MXF-XX-XX-SH-M-20003"
        assert r["project"]["project_number"] == 1234

    def test_get_documents(self):
        post_project()
        document = DocumentBasePost(project_id=1)
        post_document(document)
        response = client.get("/documents/")
        assert response.status_code == 200
        assert response.json()[0]["document_code"] == "06667-MXF-XX-XX-SH-M-20003"

    def test_patch_document(self):
        post_project()
        document = DocumentBasePost(project_id=1)
        doc = post_document(document).json()
        doc["document_code"] = "06667-MXF-XX-XX-SH-M-20004"
        response = client.patch("/document/1/", json=doc)
        assert response.status_code == 200
        assert response.json()["document_code"] == "06667-MXF-XX-XX-SH-M-20004"
