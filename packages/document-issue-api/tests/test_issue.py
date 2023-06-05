from setup_test_client import client, clean_session, get_db_path
from fastapi.encoders import jsonable_encoder
from document_issue.issue import Issue


def post_issue(issue: Issue):
    _ = jsonable_encoder(issue)
    return client.post("/issue/", json=_)


class TestIssue:
    def test_post_issue(self):
        issue = Issue()
        response = post_issue(issue)
        assert response.status_code == 200
