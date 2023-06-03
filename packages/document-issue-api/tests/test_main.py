from setup_test_client import client, clean_session, get_db_path


def test_app_exists():
    assert client
    assert get_db_path().is_file()
