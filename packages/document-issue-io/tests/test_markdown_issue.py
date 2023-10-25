import pathlib
import shutil
import pytest
from polyfactory.factories.pydantic_factory import ModelFactory

from document_issue.document_issue import DocumentIssueClassification
from document_issue_io.markdown_issue import MarkdownDocumentIssue

from tests.constants import FDIR_TEST_OUTPUT

FPTH_TEST_DOC_ISSUE = FDIR_TEST_OUTPUT / "document_issue.json"
FPTH_TEST_DOC_ISSUE_SCHEMA = FDIR_TEST_OUTPUT / "document_issue.schema.json"


@pytest.fixture(scope="class")
def refresh_dir():
    shutil.rmtree(FDIR_TEST_OUTPUT, ignore_errors=True)
    FDIR_TEST_OUTPUT.mkdir(parents=True, exist_ok=True)


class DocumentIssueFactory(ModelFactory[DocumentIssueClassification]):
    __model__ = DocumentIssueClassification


@pytest.mark.usefixtures("refresh_dir")
class TestMarkdownDocumentIssue:
    def test_create_markdown_document_issue_to_md(self):
        document_issue = DocumentIssueFactory.build()
        document_issue.project_name = "A Max Fordham Project"
        document_issue.format_configuration.date_string_format = "%d %^b %y"
        document_issue.issue_history[0].author = "OH"
        document_issue.issue_history[0].checked_by = "JG"
        document_issue.document_role[0].initials = "OH"
        markdown_document_issue = MarkdownDocumentIssue(
            document_issue,
            fpth_md_docissue=FDIR_TEST_OUTPUT / "test_basic.dh.md",
            tomd=True,
        )
        assert pathlib.Path(markdown_document_issue.fpth_md_docissue).is_file()
        # assert pathlib.Path(markdown_document_issue.fpth_docx_docissue).is_file()

    def test_create_markdown_document_issue_to_pdf(self):
        document_issue = DocumentIssueFactory.build()
        document_issue.project_name = "A Max Fordham Project"
        document_issue.format_configuration.date_string_format = "%d %^b %y"
        document_issue.issue_history[0].author = "OH"
        document_issue.issue_history[0].checked_by = "JG"
        document_issue.document_role[0].initials = "OH"
        markdown_document_issue = MarkdownDocumentIssue(
            document_issue,
            fpth_md_docissue=FDIR_TEST_OUTPUT / "test_basic.dh.md",
            tomd=True,
            to_pdf=True,
        )
        assert pathlib.Path(markdown_document_issue.fpth_md_docissue).is_file()
        assert pathlib.Path(markdown_document_issue.fpth_pdf_docissue).is_file()
