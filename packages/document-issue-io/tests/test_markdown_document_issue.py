import pytest
import shutil
import datetime
from polyfactory.factories.pydantic_factory import ModelFactory

from document_issue.document_issue import DocumentIssue, Issue
from document_issue.issue import StatusRevisionEnum
from document_issue_io.markdown_document_issue import (
    MarkdownDocumentIssue,
    document_issue_md_to_pdf,
)

from tests.constants import FDIR_TEST_OUTPUT

FPTH_TEST_DOC_ISSUE = FDIR_TEST_OUTPUT / "document_issue.json"
FPTH_TEST_DOC_ISSUE_SCHEMA = FDIR_TEST_OUTPUT / "document_issue.schema.json"


class DocumentIssueFactory(ModelFactory[DocumentIssue]):
    __model__ = DocumentIssue


def create_test_document_issue():
    return DocumentIssue(
        project_name="A Max Fordham Project",
        project_number="J4321",
        document_role=[dict(initials="OH", role_name="Director in Charge")],
        document_description="A description of a Max Fordham Project",
        name_nomenclature="project-originator-volume-level-type-role-number",
        issue_history=[
            dict(
                author="OH",
                checked_by="JG",
                revision="P01",
                status_code="S2",
                status_description="Suitable for information",
                issue_notes="This is an issue note",
            )
        ],
        format_configuration=dict(date_string_format="%d %^b %y"),
        notes=[
            "This is a note",
            "This is another note",
            (
                "This is a very long note which states something important about the"
                " document issue"
            ),
        ],
    )


class TestMarkdownDocumentIssue:
    def test_to_file(self):
        document_issue = create_test_document_issue()
        markdown_document_issue = MarkdownDocumentIssue(
            document_issue,
        )
        FPTH_MD = FDIR_TEST_OUTPUT / f"test_to_file.md"
        markdown_document_issue.to_file(FPTH_MD)
        assert FPTH_MD.is_file()


MD = """
# title

1.  One
2.  Two
3.  Three

-   convert this notebook to markdown
-   read `docissue.json`
-   convert using `document_issue_md_to_pdf`

## My Project

| Tables   |      Are      | Cool |
|----------|:-------------:|-----:|
| col 1 is |  left-aligned | 1600 |
| col 2 is |    centered   |   12 |
| col 3 is | right-aligned |    1 |
"""


class TestDocumentIssueMdToPdf:
    """Test the function `document_issue_md_to_pdf`."""

    def test_to_pdf(self):
        FDIR_RENDER = FDIR_TEST_OUTPUT / "test_to_pdf"
        shutil.rmtree(FDIR_RENDER, ignore_errors=True)
        FDIR_RENDER.mkdir(parents=True, exist_ok=True)
        document_issue = create_test_document_issue()
        document_issue.format_configuration.output_author = False
        document_issue.format_configuration.output_checked_by = False
        fpth_pdf = FDIR_RENDER / f"{document_issue.document_code}.pdf"
        document_issue_md_to_pdf(
            document_issue=document_issue,
            fpth_pdf=fpth_pdf,
        )
        assert fpth_pdf.with_suffix(".md").is_file()
        assert fpth_pdf.is_file()
        assert not (
            fpth_pdf.with_suffix(".log")
        ).is_file()  # log file should be deleted if Quarto PDF compilation is successful

    def test_to_pdf_with_markdown_content(self):
        FDIR_RENDER = FDIR_TEST_OUTPUT / "test_to_pdf_with_markdown_content"
        shutil.rmtree(FDIR_RENDER, ignore_errors=True)
        FDIR_RENDER.mkdir(parents=True, exist_ok=True)
        fpth_md = FDIR_RENDER / "test.md"
        fpth_md.write_text(MD)
        document_issue = create_test_document_issue()
        document_issue.format_configuration.output_author = False
        document_issue.format_configuration.output_checked_by = False
        fpth_pdf = FDIR_RENDER / f"{document_issue.document_code}.pdf"
        document_issue_md_to_pdf(
            document_issue=document_issue, fpth_md=fpth_md, fpth_pdf=fpth_pdf
        )
        assert fpth_pdf.is_file()
        # Check that the markdown file created contains the correct content
        assert MD in fpth_pdf.with_suffix(".md").read_text()

    def test_to_pdf_with_author(self):
        FDIR_RENDER = FDIR_TEST_OUTPUT / "test_to_pdf_with_author"
        shutil.rmtree(FDIR_RENDER, ignore_errors=True)
        FDIR_RENDER.mkdir(parents=True, exist_ok=True)
        document_issue = create_test_document_issue()
        document_issue.format_configuration.output_author = True
        document_issue.format_configuration.output_checked_by = False
        fpth_pdf = FDIR_RENDER / f"{document_issue.document_code}.pdf"
        document_issue_md_to_pdf(
            document_issue=document_issue,
            fpth_pdf=fpth_pdf,
        )
        assert fpth_pdf.with_suffix(".md").is_file()
        assert fpth_pdf.is_file()
        assert not (
            fpth_pdf.with_suffix(".log")
        ).is_file()  # log file should be deleted if Quarto PDF compilation is successful

    def test_to_pdf_with_author_and_checked_by(self):
        FDIR_RENDER = FDIR_TEST_OUTPUT / "test_to_pdf_with_author_and_checked_by"
        shutil.rmtree(FDIR_RENDER, ignore_errors=True)
        FDIR_RENDER.mkdir(parents=True, exist_ok=True)
        document_issue = create_test_document_issue()
        document_issue.format_configuration.output_author = True
        document_issue.format_configuration.output_checked_by = True
        fpth_pdf = FDIR_RENDER / f"{document_issue.document_code}.pdf"
        document_issue_md_to_pdf(
            document_issue=document_issue,
            fpth_pdf=fpth_pdf,
        )
        assert fpth_pdf.with_suffix(".md").is_file()
        assert fpth_pdf.is_file()
        assert not (
            fpth_pdf.with_suffix(".log")
        ).is_file()  # log file should be deleted if Quarto PDF compilation is successful

    def test_to_pdf_loads_of_notes_and_issues(self):
        """Test to make sure that the PDF is created when there are lots of notes and issues.
        Please check the PDF after this test to make sure that the tables are formatted correctly.
        """
        FDIR_RENDER = FDIR_TEST_OUTPUT / "test_to_pdf_loads_of_notes_and_issues"
        shutil.rmtree(FDIR_RENDER, ignore_errors=True)
        FDIR_RENDER.mkdir(parents=True, exist_ok=True)
        document_issue = create_test_document_issue()
        document_issue.document_role = document_issue.document_role * 5
        document_issue.issue_history = document_issue.issue_history * 5
        document_issue.issue_history += [
            Issue(
                author="OH",
                checked_by="JG",
                status_revision=StatusRevisionEnum.S1_P,
                date=datetime.date(2024, 1, 1),
            ),
            Issue(
                author="OH",
                checked_by="JG",
                status_revision=StatusRevisionEnum.S2_P,
                date=datetime.date(2024, 1, 1),
            ),
            Issue(
                author="OH",
                checked_by="JG",
                status_revision=StatusRevisionEnum.S3_P,
                date=datetime.date(2024, 1, 1),
            ),
            Issue(
                author="OH",
                checked_by="JG",
                status_revision=StatusRevisionEnum.S4_P,
                date=datetime.date(2024, 1, 1),
            ),
            Issue(
                author="OH",
                checked_by="JG",
                status_revision=StatusRevisionEnum.S5_P,
                date=datetime.date(2024, 1, 1),
            ),
            Issue(
                author="OH",
                checked_by="JG",
                status_revision=StatusRevisionEnum.S6_P,
                date=datetime.date(2024, 1, 1),
            ),
            Issue(
                author="OH",
                checked_by="JG",
                status_revision=StatusRevisionEnum.S7_P,
                date=datetime.date(2024, 1, 1),
            ),
            Issue(
                author="OH",
                checked_by="JG",
                status_revision=StatusRevisionEnum.S8_P,
                date=datetime.date(2024, 1, 2),
            ),
        ]
        document_issue.notes[2] = document_issue.notes[2] * 5
        document_issue.notes = document_issue.notes * 5
        document_issue.format_configuration.output_author = True
        document_issue.format_configuration.output_checked_by = True
        fpth_pdf = FDIR_RENDER / f"{document_issue.document_code}.pdf"
        document_issue_md_to_pdf(
            document_issue=document_issue,
            fpth_pdf=fpth_pdf,
        )
        assert fpth_pdf.with_suffix(".md").is_file()
        assert fpth_pdf.is_file()
        assert not (
            fpth_pdf.with_suffix(".log")
        ).is_file()  # log file should be deleted if Quarto PDF compilation is successful

    def test_to_pdf_error(self):
        """If the markdown file has the same file path as the output markdown file, raise an error."""
        FDIR_RENDER = FDIR_TEST_OUTPUT / "test_to_pdf_with_markdown_content"
        fpth_md = FDIR_RENDER / "test.md"
        fpth_pdf = FDIR_RENDER / "test.pdf"
        document_issue = create_test_document_issue()
        document_issue.format_configuration.output_author = False
        document_issue.format_configuration.output_checked_by = False
        with pytest.raises(ValueError):
            document_issue_md_to_pdf(
                document_issue=document_issue, fpth_md=fpth_md, fpth_pdf=fpth_pdf
            )
