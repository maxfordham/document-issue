from polyfactory.factories.pydantic_factory import ModelFactory

from document_issue.document_issue import DocumentIssue
from document_issue_io.title_block import (
    build_title_block_pdf,
    build_schedule_title_page_template_pdf,
)

from tests.constants import FDIR_TEST_OUTPUT


class DocumentIssueFactory(ModelFactory[DocumentIssue]):
    __model__ = DocumentIssue


def test_build_title_block_pdf():
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
    document_issue.issue_history[0].revision = "P01"
    document_issue.issue_history[0].status_code = "S2"
    document_issue.issue_history[0].status_description = "Suitable for information"

    FPTH_TITLE_BLOCK_PDF = FDIR_TEST_OUTPUT / "title-block.pdf"
    FPTH_TITLE_BLOCK_PDF.unlink(missing_ok=True)

    build_title_block_pdf(
        document_issue=document_issue, fpth_output=FPTH_TITLE_BLOCK_PDF
    )
    assert FPTH_TITLE_BLOCK_PDF.exists()


def test_build_schedule_title_page_template_pdf():
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
    document_issue.issue_history[0].revision = "P01"
    document_issue.issue_history[0].status_code = "S2"
    document_issue.issue_history[0].status_description = "Suitable for information"

    FPTH_SCHEDULE_TITLE_PAGE_PDF = FDIR_TEST_OUTPUT / "title-page.pdf"
    FPTH_SCHEDULE_TITLE_PAGE_PDF.unlink(missing_ok=True)

    build_schedule_title_page_template_pdf(
        document_issue=document_issue, fpth_output=FPTH_SCHEDULE_TITLE_PAGE_PDF
    )
    assert FPTH_SCHEDULE_TITLE_PAGE_PDF.exists()
