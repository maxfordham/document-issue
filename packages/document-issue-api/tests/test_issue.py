from setup_test_client import client, clean_session, get_db_path
from fastapi.encoders import jsonable_encoder
from document_issue.issue import Issue

from rest_funcs import post_issue, post_document


class TestIssue:
    def test_post_issue(self):
        post_document()
        response = post_issue()
        r = response.json()
        assert response.status_code == 200
        assert r['revision'] == 'P01'

    def test_get_issue(self):
        response = client.get("/issue/1")
        r = response.json()
        assert response.status_code == 200
        assert r['revision'] == 'P01'

    def test_patch_issue(self):
        response = client.patch("/issue/1", json={"revision": "P02"})
        r = response.json()
        assert response.status_code == 200
        assert r['revision'] == 'P02'

    def test_delete_issue(self):
        response = client.delete("/issue/1")
        r = response.json()
        assert response.status_code == 200
        assert r['revision'] == 'P02'
