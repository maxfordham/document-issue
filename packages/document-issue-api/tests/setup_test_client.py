import pathlib
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.encoders import jsonable_encoder

from document_issue.issue import Issue
from document_issue.person import Person
from document_issue.role import Role
from document_issue.project import ProjectBase
from document_issue_api.main import app
from document_issue_api.database import get_db
from document_issue_api.env import ApiEnv
from document_issue_api.models import Base
from document_issue_api.document.schemas import DocumentBasePost


FDIR_TEST = pathlib.Path(__file__).parent
FPTH_API_TEST_ENV = FDIR_TEST / "api-test.env"
ENV = ApiEnv(_env_file=FPTH_API_TEST_ENV, _env_file_encoding="utf-8")

# --------------- equivalent to: document_issue_api./database.py ---------------------


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def get_db_path():
    return pathlib.Path(ENV.DOCUMENTISSUE_DATABASE_URL.replace("sqlite:///", ""))


get_db_path().unlink(missing_ok=True)
engine = create_engine(ENV.DOCUMENTISSUE_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


# -------- rest_funcs.py ------------


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


def delete_role(role_id=1):
    return client.delete(f"/role/{role_id}")


def post_project_role_with_person():
    post_person()
    post_project()
    post_role()
    return client.post("/project_role/1/1/", params={"person_id": 1})


def post_project_role_with_person_and_document_role():
    assert post_project_role_with_person().status_code == 200
    assert post_document().status_code == 200
    return client.post("/document_role/1/1")


# ------------------------------------------
