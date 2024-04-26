from document_issue.document_issue import Issue
from document_issue.issue import StatusRevisionEnum


def test_Issue():
    issue = Issue()
    assert issue.revision == "P01"
    di = issue.model_dump(mode="json")
    assert di["revision"] == "P01"


def test_StatusRevisionEnum():
    """Test that all StatusRevisionEnum values are valid."""
    for enum in StatusRevisionEnum:
        issue = Issue(status_revision=enum)
        assert issue
