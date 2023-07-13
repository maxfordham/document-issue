from rest_funcs import post_project_role_with_person_and_document_role, post_issue
import pathlib
import shutil


def test_copy_testdb_to_appdb():
    """Setup a test database and copy it to the app database"""
    post_issue()
    post_project_role_with_person_and_document_role()
    p_test = pathlib.Path(__file__).parent / "test.db"
    p_app = pathlib.Path(__file__).parents[1] / "src" / "document_issue_api" / "app.db"

    p_app.unlink(missing_ok=True)
    assert not p_app.is_file()
    shutil.copyfile(p_test, p_app)
    assert p_app.is_file()
