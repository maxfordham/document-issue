from polyfactory.factories.pydantic_factory import ModelFactory
from document_issue.document_issue import DocumentIssue, DocumentRole, RoleEnum, Issue
from document_issue.enums import StatusRevisionEnum
from document_issue_io.title_block import (
    title_block_a4,
    title_block_a3,
)

from tests.constants import (
    FPTH_TITLE_BLOCK_PDF,
    FPTH_SCHEDULE_TITLE_PAGE_PDF,
    FPTH_TITLE_BLOCK_PDF_A3,
    FPTH_TITLE_BLOCK_PDF_NOMENCLATURE,
)


class DocumentIssueFactory(ModelFactory[DocumentIssue]):
    __model__ = DocumentIssue


def create_document_issue():
    issue = Issue(status_revision=StatusRevisionEnum.A4_C)
    document_issue = DocumentIssueFactory.build(
        document_role=[DocumentRole(**{"role_name": RoleEnum.director, "name": "DR"})],
        issue_history=[issue],
    )
    document_issue.project_name = (
        "A Max Fordham Project: Rotunda Refurbishment part 1 million"
    )
    document_issue.client_name = "Max Fordham LLP Partnership"
    document_issue.project_number = "J4321"
    document_issue.document_role[0].initials = "OH"
    document_issue.document_role[0].role_name = "Director in Charge"
    document_issue.document_code = "06667-MXF-XX-XX-SH-M-20003"
    document_issue.document_description = (
        "A description of a Max Fordham Project can split lines but no more than two"
    )
    document_issue.name_nomenclature = (
        "project-originator-volume-level-type-role-number"
    )
    return document_issue


def test_build_title_block_pdf():
    fpth = FPTH_TITLE_BLOCK_PDF
    document_issue = create_document_issue()
    fpth.unlink(missing_ok=True)
    title_block_a4(document_issue=document_issue, fpth_output=fpth)
    assert fpth.exists()


def test_build_title_block_pdf_name_nomenclature():
    fpth = FPTH_TITLE_BLOCK_PDF_NOMENCLATURE
    document_issue = create_document_issue()
    document_issue.name_nomenclature = (
        "originator-project-volume-level-type-role-number"
    )
    fpth.unlink(missing_ok=True)
    title_block_a4(document_issue=document_issue, fpth_output=fpth)
    assert fpth.exists()


def test_title_block_a3():
    fpth = FPTH_TITLE_BLOCK_PDF_A3
    document_issue = create_document_issue()
    fpth.unlink(missing_ok=True)
    title_block_a3(document_issue=document_issue, fpth_output=fpth)
    assert fpth.exists()


def test_title_page_a4():
    fpth = FPTH_SCHEDULE_TITLE_PAGE_PDF
    document_issue = create_document_issue()
    fpth.unlink(missing_ok=True)
    title_block_a4(
        document_issue=document_issue,
        fpth_output=fpth,
        is_titlepage=True,
    )
    assert fpth.exists()
