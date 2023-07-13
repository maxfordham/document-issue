from setup_test_client import client, clean_session, get_db_path
from fastapi.encoders import jsonable_encoder
from document_issue.issue import Issue
from document_issue.person import Person
from document_issue.role import Role
from document_issue.project import ProjectBase

from document_issue_api.document.schemas import DocumentBasePost


def post_project():
    project = ProjectBase(project_name="test_project", project_number=1234)
    _ = jsonable_encoder(project)
    return client.post("/project/", json=_)


def post_issue(issue: Issue = Issue(), document_id: int = 1):
    _ = jsonable_encoder(issue)
    return client.post(f"/issue/{str(document_id)}", json=_)


def post_document(document: DocumentBasePost = DocumentBasePost(project_id=1)):
    _ = jsonable_encoder(document)
    return client.post(f"/document/", json=_)


def post_person(initials="JG"):
    person = Person(initials=initials, full_name="test_description")
    _ = jsonable_encoder(person)
    return client.post("/person/", json=_)


def post_role(role_name="test_role"):
    role = Role(role_name=role_name, role_description="test_description")
    _ = jsonable_encoder(role)
    return client.post("/role/", json=_)


def post_project_role_with_person():
    post_person()
    post_project()
    post_role()
    return client.post("/project_role/1/1/", params={"person_id": 1})


def post_project_role_with_person_and_document_role():
    assert post_project_role_with_person().status_code == 200
    assert post_document().status_code == 200
    return client.post("/document_role/1/1")
