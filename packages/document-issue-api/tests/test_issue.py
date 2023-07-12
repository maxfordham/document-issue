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
