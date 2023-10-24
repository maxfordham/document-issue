import subprocess
import pathlib
import stringcase
import typing as ty
import pandas as pd
from tabulate import tabulate
from jinja2 import Environment, FileSystemLoader

from document_issue.document_issue import DocumentIssueClassification
from document_issue_io.constants import (
    PATH_REL_IMG,
    DIR_TEMPLATES,
    NAME_MD_DOCISSUE_TEMPLATE,
)


class MarkdownDocumentIssue:
    """Create structured markdown header from Document object"""

    def __init__(
        self,
        document_issue: DocumentIssueClassification,
        fpth_md_docissue: ty.Optional[pathlib.Path] = None,
        path_rel_img: pathlib.Path = PATH_REL_IMG,
        tomd=False,
        to_pdf=False,
    ):
        self.document_issue = document_issue
        self.tomd = tomd
        self.to_pdf = to_pdf
        self.fpth_md_docissue = fpth_md_docissue
        self.dir_md_docissue = fpth_md_docissue.parent
        self.file_loader = FileSystemLoader(DIR_TEMPLATES)
        self.env = Environment(loader=self.file_loader)
        self.path_rel_img = path_rel_img
        self.issue_history_cols = {
            "date": "date",
            "revision": "rev",
            "status_code": "status",
            "status_description": "description",
            "issue_notes": "issue notes",
        }
        self.md_col_widths = ': {tbl-colwidths="[17.5,5,7.5,25,45]"}'
        if self.document_issue.format_configuration.output_author:
            self.issue_history_cols["author"] = "author"
            self.md_col_widths = ': {tbl-colwidths="[17.5,5,7.5,25,40,5]"}'
        if self.document_issue.format_configuration.output_checked_by:
            self.issue_history_cols["checked_by"] = "checked by"
            self.md_col_widths = ': {tbl-colwidths="[17.5,5,7.5,25,35,5,5]"}'
        if fpth_md_docissue is None:
            fpth_md_docissue = pathlib.Path(self.document_issue.document_code + ".docissue.md")
        if self.tomd or self.to_pdf:
            self._tomd()
        if self.to_pdf:
            self._to_pdf()

    def _tomd(self):
        if self.fpth_md_docissue is not None:
            f = open(self.fpth_md_docissue, "w")
            f.write(self.md_docissue)
            f.close()
        else:
            raise ValueError("fpth_md_docissue not given")

    def _to_pdf(self):
        pass
        # fpth_md = self.fpth_md_docissue
        # fpth_docx = str(pathlib.Path(fpth_md).with_suffix(".docx"))
        # self.fpth_docx_docissue = fpth_docx
        # if self.fpth_refdocx.is_file():
        #     fpth_refdocx = self.fpth_refdocx
        #     cmd = f"pandoc {fpth_md} -s -f markdown -t docx -o {fpth_docx} --filter=pandoc-docx-pagebreakpy --reference-doc={fpth_refdocx} --columns=6"
        # else:
        #     cmd = f"pandoc {fpth_md} -s -f markdown -t docx -o {fpth_docx} --filter=pandoc-docx-pagebreakpy --columns=6"
        # subprocess.run(cmd.split(" "))

    @property
    def md_issue_history(self):
        df = self.document_issue.df_issue_history[self.issue_history_cols.keys()]
        df = df.rename(columns=self.issue_history_cols)
        md_df = df.set_index(
            'date'
        ).to_markdown()
        return md_df + "\n\n" + self.md_col_widths

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
