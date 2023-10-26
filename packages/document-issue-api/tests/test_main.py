from setup_test_client import client, get_db_path


def test_app_exists():
    assert client
    assert get_db_path().is_file()
