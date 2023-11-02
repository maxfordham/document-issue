import pathlib
import typing as ty
from jinja2 import Environment, FileSystemLoader

from document_issue.document_issue import DocumentIssue
from document_issue_io.constants import (
    FDIR_TEMPLATES,
    NAME_MD_DOCISSUE_TEMPLATE,
)
from document_issue_io.utils import (
    document_issue_md_to_pdf,
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
        col_widths = ': {tbl-colwidths="[17.5,5,7.5,25,45]"}'
        if self.document_issue.format_configuration.output_author:
            col_widths = ': {tbl-colwidths="[17.5,5,7.5,25,32.5,12.5]"}'
            if self.document_issue.format_configuration.output_checked_by:
                col_widths = ': {tbl-colwidths="[17.5,5,7.5,20,25,10,15]"}'
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

    def to_file(self, fpth_md: pathlib.Path):
        """Create markdown file from DocumentIssue object"""
        f = open(fpth_md, "w")
        f.write(self.md_docissue)
        f.close()

    def to_pdf(self, fpth_md: pathlib.Path, fpth_pdf: pathlib.Path):
        """Create pdf file from markdown file using quarto."""
        self.to_file(fpth_md)
        document_issue_md_to_pdf(
            document_issue=self.document_issue,
            fpth_md=fpth_md,
            fpth_pdf=fpth_pdf,
        )
