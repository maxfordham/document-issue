from document_issue.document_issue import DocumentIssue, Issue, DocumentIssueV2
from document_issue.issue import StatusRevisionEnum
import pathlib

DIR_TESTS = pathlib.Path(__file__).parent


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


def test_current_issue():
    """Test that the current issue property gets the latest issue (by date)."""
    document_issue = DocumentIssue(client_name="Test Client")
    document_issue.issue_history = [
        Issue(
            revision="P01",
            status_revision=StatusRevisionEnum.S0_P,
            date="2021-01-01",
        ),
        Issue(
            revision="P02",
            status_revision=StatusRevisionEnum.S2_P,
            date="2021-01-02",
        ),
        Issue(
            revision="P03",
            status_revision=StatusRevisionEnum.S3_P,
            date="2021-01-03",
        ),
    ]
    assert document_issue.current_issue.status_revision == StatusRevisionEnum.S3_P.value
    fdir = DIR_TESTS / "test_document_issue"
    fdir.mkdir(exist_ok=True)
    p = fdir / "document_issue.json"
    p.write_text(document_issue.model_dump_json(indent=4))
    assert p.exists()
