import pathlib

from document_issue.document_issue import DocumentIssue
from document_issue_io.markdown_document_issue import (
    generate_pdf_report,
)


document_issue = DocumentIssue(
    project_name="A Max Fordham Project & Co",
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


def create_pdf_report():
    FDIR_RENDER = pathlib.Path(__file__).parent
    document_issue.format_configuration.output_author = False
    document_issue.format_configuration.output_checked_by = False
    fpth_pdf = FDIR_RENDER / f"{document_issue.document_code}.pdf"
    generate_pdf_report(
        document_issue=document_issue,
        fpth_pdf=fpth_pdf,
    )
    assert fpth_pdf.with_suffix(".md").is_file()
    assert fpth_pdf.is_file()
    assert not (
        fpth_pdf.with_suffix(".log")
    ).is_file()  # log file should be deleted if Quarto PDF compilation is successful


if __name__ == "__main__":
    create_pdf_report()
