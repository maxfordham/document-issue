import pytest
from setup_test_client import (
    client,
    post_project,
    post_document,
)


def delete_document(document_id=1):
    return client.delete(f"/document/{document_id}")


def delete_project(project_id=1):
    return client.delete(f"/project/{project_id}")


@pytest.fixture
def post_document_then_delete():
    _ = post_project()
    r = post_document()
    id_ = r.json()["id"]
    p_id_ = 1
    yield r
    delete_document(id_)
    delete_project(p_id_)

# NOTE: currently broken test. also broken when manually testing in swagger API. 
def test_post_document(post_document_then_delete):
    response = post_document_then_delete
    assert response.status_code == 200
    assert isinstance(response.json()["document_code"], str)


# def test_get_document(post_document_then_delete):
#     response = post_document_then_delete
#     document_id = response.json()["id"]
#     response = client.get(f"/document/{document_id}")
#     assert response.status_code == 200
#     assert isinstance(response.json()["document_code"], str)


# def test_get_documents(post_document_then_delete):
#     response = post_document_then_delete
#     r = client.get(f"/documents/")
#     assert r.status_code == 200
#     # assert response.json()[0]["document_code"] == "06667-MXF-XX-XX-SH-M-20003"


# def test_patch_document(post_document_then_delete):
#     response = post_document_then_delete
#     document_id = response.json()["id"]
#     response = client.patch(f"/document/{document_id}", json={"document_code": "06667-MXF-XX-XX-SH-M-20004"})
#     assert response.status_code == 200
#     assert response.json()["document_code"] == "06667-MXF-XX-XX-SH-M-20004"


# def test_delete_document():
#     _ = post_project()
#     r = post_document()
#     assert r.status_code == 200
#     id_ = r.json()["id"]
#     response = client.delete(f"/document/{id_}")
#     assert response.status_code == 200
#     assert response.json()["document_code"] == "06667-MXF-XX-XX-SH-M-20003"
#     response = client.get(f"/document/{id_}")
#     assert response.status_code == 404


# @pytest.mark.usefixtures("clear_data_func")
# class TestDocument:
#     def test_post_document(self):
#         post_project()
#         response = post_document()
#         assert response.status_code == 200
#         assert response.json()["document_code"] == "06667-MXF-XX-XX-SH-M-20003"

#     def test_get_document(self):
#         post_project()
#         post_document()
#         response = client.get("/document/1/")
#         assert response.status_code == 200
#         assert response.json()["document_code"] == "06667-MXF-XX-XX-SH-M-20003"

#     def test_get_document_issue(self):
#         post_project_role_with_person_and_document_role()
#         post_issue()
#         response = client.get("/document_issue/1/")
#         assert response.status_code == 200
#         r = response.json()
#         assert r["document_code"] == "06667-MXF-XX-XX-SH-M-20003"
#         assert r["project"]["project_number"] == 1234
#         assert r["issue"][0]["revision"] == "P01"
#         assert r["document_role"][0]["role"]["role_name"] == "test_role"

#     def test_get_documents(self):
#         post_project()
#         post_document()
#         response = client.get("/documents/")
#         assert response.status_code == 200
#         assert response.json()[0]["document_code"] == "06667-MXF-XX-XX-SH-M-20003"

#     def test_patch_document(self):
#         post_project()
#         doc = post_document().json()
#         doc["document_code"] = "06667-MXF-XX-XX-SH-M-20004"
#         response = client.patch("/document/1/", json=doc)
#         assert response.status_code == 200
#         assert response.json()["document_code"] == "06667-MXF-XX-XX-SH-M-20004"
