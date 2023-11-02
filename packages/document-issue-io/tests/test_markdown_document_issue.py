import pathlib
import shutil
import pytest
from polyfactory.factories.pydantic_factory import ModelFactory

from document_issue.document_issue import DocumentIssue
from document_issue_io.markdown_document_issue import MarkdownDocumentIssue

from tests.constants import FDIR_TEST_OUTPUT

FPTH_TEST_DOC_ISSUE = FDIR_TEST_OUTPUT / "document_issue.json"
FPTH_TEST_DOC_ISSUE_SCHEMA = FDIR_TEST_OUTPUT / "document_issue.schema.json"


class DocumentIssueFactory(ModelFactory[DocumentIssue]):
    __model__ = DocumentIssue


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
    document_issue.notes = [
        "This is a note",
        "This is another note",
        (
            "This is a very long note which states something important about the"
            " document issue"
        ),
    ]
    return document_issue


class TestMarkdownDocumentIssue:
    def test_to_file(self):
        document_issue = create_test_document_issue()
        markdown_document_issue = MarkdownDocumentIssue(
            document_issue,
        )
        FPTH_MD = FDIR_TEST_OUTPUT / "test_to_file.docissue.md"
        markdown_document_issue.to_file(FPTH_MD)
        assert pathlib.Path(FPTH_MD).is_file()

    def test_to_pdf(self):
        FDIR_RENDER = FDIR_TEST_OUTPUT / "render" / "test_to_pdf"
        FPTH_MD = FDIR_RENDER / "test_to_pdf.docissue.md"
        FPTH_PDF = FDIR_TEST_OUTPUT / "test_to_pdf.docissue.pdf"
        shutil.rmtree(FDIR_RENDER, ignore_errors=True)
        FDIR_RENDER.mkdir(parents=True, exist_ok=True)
        document_issue = create_test_document_issue()
        document_issue.format_configuration.output_author = False
        document_issue.format_configuration.output_checked_by = False
        markdown_document_issue = MarkdownDocumentIssue(
            document_issue,
        )
        markdown_document_issue.to_pdf(
            FPTH_MD,
            FPTH_PDF,
        )
        assert pathlib.Path(FPTH_MD).is_file()
        assert pathlib.Path(FPTH_PDF).is_file()
        FPTH_LOG = FDIR_RENDER / "test_to_pdf.docissue.log"
        assert (
            not FPTH_LOG.is_file()
        )  # log file should be deleted if Quarto PDF compilation is successful

    def test_to_pdf_with_author(self):
        FDIR_RENDER = FDIR_TEST_OUTPUT / "render" / "test_to_pdf_with_author"
        FPTH_MD = FDIR_RENDER / "test_to_pdf_with_author.docissue.md"
        FPTH_PDF = FDIR_TEST_OUTPUT / "test_to_pdf_with_author.docissue.pdf"
        shutil.rmtree(FDIR_RENDER, ignore_errors=True)
        FDIR_RENDER.mkdir(parents=True, exist_ok=True)
        document_issue = create_test_document_issue()
        document_issue.format_configuration.output_author = True
        document_issue.format_configuration.output_checked_by = False
        markdown_document_issue = MarkdownDocumentIssue(
            document_issue,
        )
        markdown_document_issue.to_pdf(
            FPTH_MD,
            FPTH_PDF,
        )
        assert pathlib.Path(FPTH_MD).is_file()
        assert pathlib.Path(FPTH_PDF).is_file()
        FPTH_LOG = FDIR_RENDER / "test_to_pdf_with_author.docissue.log"
        assert (
            not FPTH_LOG.is_file()
        )  # log file should be deleted if Quarto PDF compilation is successful

    def test_to_pdf_with_author_and_checked_by(self):
        FDIR_RENDER = (
            FDIR_TEST_OUTPUT / "render" / "test_to_pdf_with_author_and_checked_by"
        )
        FPTH_MD = FDIR_RENDER / "test_to_pdf_with_author_and_checked_by.docissue.md"
        FPTH_PDF = (
            FDIR_TEST_OUTPUT / "test_to_pdf_with_author_and_checked_by.docissue.pdf"
        )
        shutil.rmtree(FDIR_RENDER, ignore_errors=True)
        FDIR_RENDER.mkdir(parents=True, exist_ok=True)
        document_issue = create_test_document_issue()
        document_issue.format_configuration.output_author = True
        document_issue.format_configuration.output_checked_by = True
        markdown_document_issue = MarkdownDocumentIssue(
            document_issue,
        )
        markdown_document_issue.to_pdf(
            FPTH_MD,
            FPTH_PDF,
        )
        assert pathlib.Path(FPTH_MD).is_file()
        assert pathlib.Path(FPTH_PDF).is_file()
        FPTH_LOG = FDIR_RENDER / "test_to_pdf_with_author_and_checked_by.docissue.log"
        assert (
            not FPTH_LOG.is_file()
        )  # log file should be deleted if Quarto PDF compilation is successful
