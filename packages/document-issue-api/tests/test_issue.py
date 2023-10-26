import pytest
from setup_test_client import client, get_db_path
from fastapi.encoders import jsonable_encoder
from document_issue.issue import Issue

from setup_test_client import post_issue, post_document


def delete_issue(issue_id=1):
    return client.delete(f"/issue/{issue_id}")


@pytest.fixture
def post_issue_then_delete():
    r = post_issue()
    assert r.status_code == 200
    id_ = r.json()["id"]
    yield r
    delete_issue(id_)


def test_post_issue(post_issue_then_delete):
    response = post_issue_then_delete
    assert response.status_code == 200
    assert response.json()["revision"] == "P01"


def test_get_issue(post_issue_then_delete):
    response = post_issue_then_delete
    issue_id = response.json()["id"]
    response = client.get(f"/issue/{issue_id}")
    assert response.status_code == 200
    assert response.json()["revision"] == "P01"


def test_patch_issue(post_issue_then_delete):
    response = post_issue_then_delete
    issue_id = response.json()["id"]
    response = client.patch(f"/issue/{issue_id}", json={"revision": "P02"})
    assert response.status_code == 200
    assert response.json()["revision"] == "P02"


def test_delete_issue():
    r = post_issue()
    assert r.status_code == 200
    id_ = r.json()["id"]
    response = client.delete(f"/issue/{id_}")
    assert response.status_code == 200
    assert response.json()["revision"] == "P01"
    response = client.get(f"/issue/{id_}")
    assert response.status_code == 404
