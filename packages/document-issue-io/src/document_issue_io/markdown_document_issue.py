import pathlib
import shutil
import subprocess
import typing as ty
from jinja2 import Environment, FileSystemLoader

from document_issue.document_issue import DocumentIssue
from document_issue_io.title_block import build_schedule_title_page_template_pdf

from document_issue_io.constants import (
    FDIR_TEMPLATES,
    NAME_MD_DOCISSUE_TEMPLATE,
)
from document_issue_io.utils import (
    change_dir,
    install_or_update_document_issue_quarto_extension,
    FPTH_FOOTER_LOGO,
)


class MarkdownDocumentIssue:
    """Create structured markdown header from Document object"""

    def __init__(
        self,
        document_issue: DocumentIssue,
    ):
        self.document_issue = document_issue
        self.file_loader = FileSystemLoader(FDIR_TEMPLATES)
        self.env = Environment(loader=self.file_loader)

    @property
    def md_issue_history_col_widths(self):
        col_widths = ': {tbl-colwidths="[12,5,7.5,30,45.5]"}'
        if self.document_issue.format_configuration.output_author:
            col_widths = ': {tbl-colwidths="[12,5,7.5,30,35,10.5]"}'
            if self.document_issue.format_configuration.output_checked_by:
                col_widths = ': {tbl-colwidths="[12,5,7.5,30,30,7,8.5]"}'
        return col_widths

    @property
    def md_issue_history(self):
        return (
            self.document_issue.issue_history_table
            + "\n\n"
            + self.md_issue_history_col_widths
        )

    @property
    def md_roles(self):
        return self.document_issue.roles_table

    @property
    def md_notes(self):
        return self.document_issue.notes_table

    @property
    def md_docissue(self):
        template = self.env.get_template(NAME_MD_DOCISSUE_TEMPLATE)
        return template.render(
            project_name=self.document_issue.project_name,
            project_number=self.document_issue.project_number,
            director_in_charge=self.document_issue.director_in_charge,
            document_description=self.document_issue.document_description,
            document_code=self.document_issue.document_code,
            name_nomenclature=self.document_issue.name_nomenclature,
            current_issue_date=self.document_issue.current_issue.date,
            current_issue_revision=self.document_issue.current_issue.revision,
            current_issue_status_code=self.document_issue.current_issue.status_code,
            current_issue_status_description=self.document_issue.current_issue.status_description,
            md_issue_history=self.md_issue_history,
            md_roles=self.md_roles,
            md_notes=self.md_notes,
        )

    def to_file(self, fpth: pathlib.Path):
        """Create markdown file from DocumentIssue object."""
        f = open(fpth, "w")
        f.write(self.md_docissue)
        f.close()


def check_markdown_file_paths(fpth_md: pathlib.Path, fpth_md_output: pathlib.Path):
    """Check if input and output markdown files are the same."""
    if fpth_md == fpth_md_output:
        raise ValueError(
            f"Input and output markdown file paths must be different. Please change file name of input markdown."
        )


def run_quarto(fpth_md_output: pathlib.Path, fpth_pdf: pathlib.Path):
    """Run quarto to convert markdown to pdf using document-issue-pdf quarto extension."""
    return subprocess.run(
        [
            "quarto",
            "render",
            fpth_md_output.name,
            "--to",
            "document-issue-pdf",
            "-o",
            fpth_pdf.name,
        ]
    )


def document_issue_md_to_pdf(
    document_issue: DocumentIssue,
    fpth_pdf: pathlib.Path,
    fpth_md: ty.Union[pathlib.Path, None] = None,
):
    """Convert markdown document issue to pdf using quarto.
    The files will be built in the parent directory of fpth_pdf."""
    fpth_md_output = fpth_pdf.parent / (fpth_pdf.stem + ".md")
    if fpth_md is not None:
        check_markdown_file_paths(fpth_md, fpth_md_output)
        md_content = fpth_md.read_text()
    else:
        md_content = ""
    with change_dir(fpth_pdf.parent):
        shutil.copy(
            FPTH_FOOTER_LOGO, FPTH_FOOTER_LOGO.name
        )  # Copy footer logo to markdown document issue directory
        build_schedule_title_page_template_pdf(document_issue=document_issue)
        install_or_update_document_issue_quarto_extension()
        markdown = MarkdownDocumentIssue(document_issue).md_docissue + md_content
        fpth_md_output.write_text(markdown)
        completed_process = run_quarto(fpth_md_output, fpth_pdf)
    return fpth_pdf
