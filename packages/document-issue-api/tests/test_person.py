from setup_test_client import client, clean_session, get_db_path, clear_data_func
from fastapi.encoders import jsonable_encoder
from document_issue.person import Person
import pytest

# from polyfactory.factories import ModelFactory


def post_person(initials="JG"):
    person = Person(initials=initials, full_name="test_description")
    _ = jsonable_encoder(person)
    return client.post("/person/", json=_)


@pytest.mark.usefixtures("clear_data_func")
class TestPerson:
    def test_post_person(self):
        response = post_person()
        assert response.status_code == 200
        assert response.json()["initials"] == "JG"

    def test_get_person(self):
        response = post_person()
        person_id = response.json()["id"]
        response = client.get(f"/person/{person_id}")
        assert response.status_code == 200
        assert response.json()["initials"] == "JG"

    def test_get_people(self):
        response = post_person()
        response = client.get(f"/person/")
        assert response.status_code == 200
        assert response.json()[0]["initials"] == "JG"

    def test_get_people_limit(self):
        response = post_person()
        response = client.get(f"/person/?limit=1")
        assert response.status_code == 200
        assert response.json()[0]["initials"] == "JG"

    def test_get_people_skip(self):
        response = post_person()
        response = client.get(f"/person/?skip=1")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_people_skip_limit(self):
        response = post_person()
        response = client.get(f"/person/?skip=1&limit=1")
        assert response.status_code == 200
        assert response.json() == []

    def test_patch_person(self):
        response = post_person()
        person_id = response.json()["id"]
        response = client.patch(f"/person/{person_id}", json={"initials": "JG2", "full_name": "new name"})
        assert response.status_code == 200
        assert response.json()["initials"] == "JG2"

    def test_delete_person(self):
        response = post_person()
        person_id = response.json()["id"]
        response = client.delete(f"/person/{person_id}")
        assert response.status_code == 200
        assert response.json()["initials"] == "JG"
