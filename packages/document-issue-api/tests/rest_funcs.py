from setup_test_client import client, clean_session, get_db_path
from fastapi.encoders import jsonable_encoder
from document_issue.issue import Issue
from document_issue_api.document.schemas import DocumentBasePost


def post_issue(issue: Issue = Issue(), document_id: int = 1):
    _ = jsonable_encoder(issue)
    return client.post(f"/issue/{str(document_id)}", json=_)


def post_document(document: DocumentBasePost = DocumentBasePost(project_id=1)):
    _ = jsonable_encoder(document)
    return client.post(f"/document/", json=_)
