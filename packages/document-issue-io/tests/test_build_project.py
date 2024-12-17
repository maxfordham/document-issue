import pathlib
import shutil
import subprocess

from document_issue_io.markdown_document_issue import (
    MarkdownDocumentIssue,
    DocumentIssue,
    install_or_update_document_issue_quarto_extension,
    build_schedule_title_page_template_pdf,
)
from document_issue_io.utils import (
    change_dir,
    FPTH_FOOTER_LOGO,
)

FDIR = pathlib.Path(__file__).parent.parent / "example-projects" / "spec-1"


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


def test_build_project():
    document_issue = create_test_document_issue()
    markdown_issue = MarkdownDocumentIssue(document_issue=document_issue)
    with change_dir(FDIR):
        shutil.copy(
            FPTH_FOOTER_LOGO, FPTH_FOOTER_LOGO.name
        )  # Copy footer logo to markdown document issue directory
        build_schedule_title_page_template_pdf(document_issue=document_issue)
        install_or_update_document_issue_quarto_extension()
        markdown_issue.to_file(pathlib.Path("document-issue.md"))

        cmd = [
            "quarto",
            "render",
            ".",
        ]
        completed_process = subprocess.run(cmd)
    print("done")
