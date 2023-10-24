import subprocess
import pathlib
import stringcase
import typing as ty
import pandas as pd
from tabulate import tabulate
from jinja2 import Environment, FileSystemLoader

from document_issue.document_issue import DocumentIssueClassification
from document_issue_io.utils import make_disclaimer_spacer
from document_issue_io.constants import (
    PATH_REL_IMG,
    PATH_REFERENCE_DOCX,
    DIR_TEMPLATES,
    NAME_MD_DISCLAIMER_TEMPLATE,
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
        issue_history_cols = [
            "date",
            "revision",
            "status_code",
            "status_description",
            "issue_notes",
        ]
        if self.document_issue.format_configuration.output_author:
            issue_history_cols += ["author"]
        if self.document_issue.format_configuration.output_checked_by:
            issue_history_cols += ["checked_by"]

        self.file_loader = FileSystemLoader(DIR_TEMPLATES)
        self.env = Environment(loader=self.file_loader)
        self.path_rel_img = path_rel_img
        if fpth_md_docissue is None:
            fpth_md_docissue = pathlib.Path(self.document_issue.document_code + ".docissue.md")
        self.fpth_md_docissue = fpth_md_docissue
        self.dir_md_docissue = fpth_md_docissue.parent
        self.dir_disclaimer_spacer = (
            self.dir_md_docissue / self.path_rel_img
        ).resolve()
        self.path_disclaimer_spacer = (
            self.dir_disclaimer_spacer / "disclaimer_spacer.png"
        )
        self.issue_history_cols = issue_history_cols
        self.tomd = tomd
        if to_pdf:
            self.tomd = True
        self.to_pdf = to_pdf
        self.disclaimer = self._disclaimer()
        if self.tomd:
            self._tomd()
        if self.to_pdf:
            self._to_pdf()

    def _disclaimer(self):
        if not self.path_disclaimer_spacer.is_file():
            self.dir_disclaimer_spacer.mkdir(exist_ok=True)

            make_disclaimer_spacer(self.dir_disclaimer_spacer)
        template = self.env.get_template(NAME_MD_DISCLAIMER_TEMPLATE)
        return template.render(fdirRelImg=self.path_rel_img)

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

    # @property
    # def md_datetime(self):
    #     return self.document_issue.date.strftime(
    #         self.document_issue.format_configuration.date_string_format
    #     )

    @property
    def md_current_issue_header_table(self):
        cols = [
            f"[{l}]" + "{custom-style='mf_headertitles'}"
            for l in list(self.document_issue.df_current_issue_header_table.reset_index())
        ]
        vals = [
            f"__{l}__"
            for l in list(self.document_issue.df_current_issue_header_table.reset_index().loc[0])
        ]
        df = pd.DataFrame.from_dict({"cols": cols, "vals": vals}).T
        md = tabulate(df, showindex=False, tablefmt="grid")
        return [f"        {l}" for l in md.splitlines()]

    @property
    def md_issue_history(self):
        df = self.document_issue.df_issue_history[self.issue_history_cols]
        newcols = [
            stringcase.sentencecase(col).lower() for col in self.issue_history_cols
        ]
        renamecols = dict(zip(self.issue_history_cols, newcols))
        df = df.rename(columns=renamecols)
        df = df.rename(
            columns={"date": 'date<span custom-style="mf_black">..........</span>'}
        )  # TODO: this is a hack. it is to ensure the column width in word
        return df.set_index(
            'date<span custom-style="mf_black">..........</span>'
        ).to_markdown()

    @property
    def md_roles(self):
        return self.document_issue.df_roles.to_markdown()

    @property
    def md_notes(self):
        return self.document_issue.df_notes.to_markdown()

    @property
    def md_doc_info(self):
        return f"""
### ISSUE HISTORY
{self.md_issue_history}
\\
\\
\\
\\
\\

### MAX FORDHAM LLP TEAM CONTRIBUTORS
{self.md_roles}
\\
\\
\\

### NOTES
{self.md_notes}


"""

    @property
    def md_page_two(self):
        df_page2 = pd.DataFrame.from_dict(
            {"disclaimer": [self.disclaimer], "docinfo": [self.md_doc_info]}
        )
        return tabulate(df_page2, showindex=False, tablefmt="grid")

    @property
    def md_docissue(self):
        template = self.env.get_template(NAME_MD_DOCISSUE_TEMPLATE)
        return template.render(
            project_name=self.document_issue.project_name,
            document_description=self.document_issue.document_description,
            current_status_description=self.document_issue.current_status_description,
            author=self.document_issue.originator,
            current_issue_long_date=self.document_issue.current_issue_long_date,
            document_code=self.document_issue.document_code,
            li_current_issue_header_table=self.md_current_issue_header_table,
            md_page_two=self.md_page_two,
        )
