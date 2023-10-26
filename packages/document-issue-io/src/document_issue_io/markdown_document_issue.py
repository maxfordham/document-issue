import os
import subprocess
import pathlib
import shutil
import typing as ty
from jinja2 import Environment, FileSystemLoader

from document_issue.document_issue import DocumentIssueClassification
from document_issue_io.title_block import build_schedule_title_page_template_pdf
from document_issue_io.constants import (
    FDIR_TEMPLATES,
    FDIR_MEDIA,
    NAME_MD_DOCISSUE_TEMPLATE,
)
from document_issue_io.utils import (
    change_dir,
    install_or_update_document_issue_quarto_extension,
)

FPTH_FOOTER_LOGO = FDIR_MEDIA / "footer-logo.png"


class MarkdownDocumentIssue:
    """Create structured markdown header from Document object"""

    def __init__(
        self,
        document_issue: DocumentIssueClassification,
        fpth_md: ty.Optional[pathlib.Path] = None,
        fpth_pdf: ty.Optional[pathlib.Path] = None,
        to_md=True,
        to_pdf=False,
    ):
        self.document_issue = document_issue
        self.to_md = to_md
        self.to_pdf = to_pdf
        self.fpth_md = fpth_md
        self.fpth_pdf = fpth_pdf
        self.dir_md_docissue = fpth_md.parent
        self.file_loader = FileSystemLoader(FDIR_TEMPLATES)
        self.env = Environment(loader=self.file_loader)
        if self.fpth_md is None:
            self.fpth_md = pathlib.Path(
                self.document_issue.document_code + ".docissue.md"
            )
        if self.fpth_pdf is None:
            self.fpth_pdf = pathlib.Path(
                self.document_issue.document_code + ".docissue.pdf"
            )
        if self.to_md or self.to_pdf:
            self._to_md()
        if self.to_pdf:
            self._to_pdf()

    def _define_issue_history_cols(self):
        self.issue_history_cols = {
            "date": "date",
            "revision": "rev",
            "status_code": "status",
            "status_description": "description",
            "issue_notes": "issue notes",
        }
        self.md_issue_history_col_widths = ': {tbl-colwidths="[17.5,5,7.5,25,45]"}'
        if self.document_issue.format_configuration.output_author:
            self.issue_history_cols["author"] = "author"
            self.md_issue_history_col_widths = (
                ': {tbl-colwidths="[17.5,5,7.5,25,35,10]"}'
            )
            if self.document_issue.format_configuration.output_checked_by:
                self.issue_history_cols["checked_by"] = "checked by"
                self.md_issue_history_col_widths = (
                    ': {tbl-colwidths="[17.5,5,7.5,25,25,10,10]"}'
                )

    def _to_md(self):
        if self.fpth_md is not None:
            f = open(self.fpth_md, "w")
            f.write(self.md_docissue)
            f.close()
        else:
            raise ValueError("fpth_md not given")

    def _to_pdf(self):
        with change_dir(self.dir_md_docissue):
            shutil.copy(FPTH_FOOTER_LOGO, FPTH_FOOTER_LOGO.name)
            build_schedule_title_page_template_pdf(document_issue=self.document_issue)
            install_or_update_document_issue_quarto_extension()
            subprocess.run(
                [
                    "quarto",
                    "render",
                    self.fpth_md.name,
                    "--to",
                    "document-issue-pdf",
                    "-o",
                    self.fpth_pdf.name,
                ]
            )
            # NOTE: quarto render does not allow to specify a relative or absolute
            # path for "-o" parameter. Therefore, will just move post-render
            if self.fpth_pdf != self.dir_md_docissue / self.fpth_pdf.name:
                shutil.move(self.fpth_pdf.name, self.fpth_pdf)

    @property
    def md_issue_history(self):
        self._define_issue_history_cols()
        df = self.document_issue.df_issue_history[self.issue_history_cols.keys()]
        df = df.rename(columns=self.issue_history_cols)
        md_df = df.set_index("date").to_markdown()
        return md_df + "\n\n" + self.md_issue_history_col_widths

    @property
    def md_roles(self):
        return self.document_issue.df_roles.to_markdown()

    @property
    def md_notes(self):
        return self.document_issue.df_notes.to_markdown()

    @property
    def md_docissue(self):
        template = self.env.get_template(NAME_MD_DOCISSUE_TEMPLATE)
        return template.render(
            project_name=self.document_issue.project_name,
            document_description=self.document_issue.document_description,
            md_issue_history=self.md_issue_history,
            md_roles=self.md_roles,
            md_notes=self.md_notes,
        )
