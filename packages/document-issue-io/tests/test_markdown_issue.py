import pathlib
import shutil
import pytest
from polyfactory.factories.pydantic_factory import ModelFactory

from document_issue.document_issue import DocumentIssueClassification
from document_issue_io.markdown_issue import MarkdownDocumentIssue

from tests.constants import FDIR_TEST_OUTPUT

FPTH_TEST_DOC_ISSUE = FDIR_TEST_OUTPUT / "document_issue.json"
FPTH_TEST_DOC_ISSUE_SCHEMA = FDIR_TEST_OUTPUT / "document_issue.schema.json"


class DocumentIssueFactory(ModelFactory[DocumentIssueClassification]):
    __model__ = DocumentIssueClassification


def create_test_document_issue():
    document_issue = DocumentIssueFactory.build()
    document_issue.project_name = "A Max Fordham Project"
    document_issue.project_number = "J4321"
    document_issue.document_role[0].initials = "OH"
    document_issue.document_role[0].role_name = "Director in Charge"
    document_issue.document_code = "06667-MXF-XX-XX-SH-M-20003"
    document_issue.document_description = "A description of a Max Fordham Project"
    document_issue.name_nomenclature = (
        "project-originator-volume-level-type-role-number"
    )
    document_issue.issue_history[0].author = "OH"
    document_issue.issue_history[0].checked_by = "JG"
    document_issue.issue_history[0].revision = "P01"
    document_issue.issue_history[0].status_code = "S2"
    document_issue.issue_history[0].status_description = "Suitable for information"
    document_issue.issue_history[0].issue_notes = "This is an issue note"
    document_issue.format_configuration.date_string_format = "%d %^b %y"
    return document_issue


class TestMarkdownDocumentIssue:
    def test_to_md(self):
        document_issue = create_test_document_issue()
        markdown_document_issue = MarkdownDocumentIssue(
            document_issue,
            fpth_md=FDIR_TEST_OUTPUT / "test_to_md.docissue.md",
            to_md=True,
        )
        assert pathlib.Path(markdown_document_issue.fpth_md).is_file()

    def test_to_pdf(self):
        FDIR_RENDER = FDIR_TEST_OUTPUT / "render" / "test_to_pdf"
        shutil.rmtree(FDIR_RENDER, ignore_errors=True)
        FDIR_RENDER.mkdir(parents=True, exist_ok=True)
        document_issue = create_test_document_issue()
        document_issue.format_configuration.output_author = False
        document_issue.format_configuration.output_checked_by = False
        markdown_document_issue = MarkdownDocumentIssue(
            document_issue,
            fpth_md=FDIR_RENDER / "test_to_pdf.docissue.md",
            fpth_pdf=FDIR_TEST_OUTPUT / "test_to_pdf.docissue.pdf",
            to_md=True,
            to_pdf=True,
        )
        assert pathlib.Path(markdown_document_issue.fpth_md).is_file()
        assert pathlib.Path(markdown_document_issue.fpth_pdf).is_file()

    def test_to_pdf_with_author(self):
        FDIR_RENDER = FDIR_TEST_OUTPUT / "render" / "test_to_pdf_with_author"
        shutil.rmtree(FDIR_RENDER, ignore_errors=True)
        FDIR_RENDER.mkdir(parents=True, exist_ok=True)
        document_issue = create_test_document_issue()
        document_issue.format_configuration.output_author = True
        document_issue.format_configuration.output_checked_by = False
        markdown_document_issue = MarkdownDocumentIssue(
            document_issue,
            fpth_md=FDIR_RENDER / "test_to_pdf_with_author.docissue.md",
            fpth_pdf=FDIR_TEST_OUTPUT / "test_to_pdf_with_author.docissue.pdf",
            to_md=True,
            to_pdf=True,
        )
        assert pathlib.Path(markdown_document_issue.fpth_md).is_file()
        assert pathlib.Path(markdown_document_issue.fpth_pdf).is_file()

    def test_to_pdf_with_author_and_checked_by(self):
        FDIR_RENDER = (
            FDIR_TEST_OUTPUT / "render" / "test_to_pdf_with_author_and_checked_by"
        )
        shutil.rmtree(FDIR_RENDER, ignore_errors=True)
        FDIR_RENDER.mkdir(parents=True, exist_ok=True)
        document_issue = create_test_document_issue()
        document_issue.format_configuration.output_author = True
        document_issue.format_configuration.output_checked_by = True
        markdown_document_issue = MarkdownDocumentIssue(
            document_issue,
            fpth_md=FDIR_RENDER / "test_to_pdf_with_author_and_checked_by.docissue.md",
            fpth_pdf=FDIR_TEST_OUTPUT
            / "test_to_pdf_with_author_and_checked_by.docissue.pdf",
            to_md=True,
            to_pdf=True,
        )
        assert pathlib.Path(markdown_document_issue.fpth_md).is_file()
        assert pathlib.Path(markdown_document_issue.fpth_pdf).is_file()
