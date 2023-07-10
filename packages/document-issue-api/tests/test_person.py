from setup_test_client import client, clean_session, get_db_path, clear_data_func
from fastapi.encoders import jsonable_encoder
from document_issue.person import Person
import pytest

# from polyfactory.factories import ModelFactory


def post_person(initials="JG"):
    person = Person(initals=initials, full_name="test_description")
    _ = jsonable_encoder(person)
    return client.post("/person/", json=_)


@pytest.mark.usefixtures("clear_data_func")
class TestPerson:
    def test_post_person(self):
        response = post_person()
        assert response.status_code == 200
        assert response.json()["initials"] == "JG"
