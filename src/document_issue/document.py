# document
"""
object model for defining the fields required for a structured document (TODO: add iso reference here)
"""
import pathlib
import pandas as pd  # TODO: remove pandas ?
import datetime
import json
import subprocess
import stringcase
from jinja2 import Environment, FileSystemLoader
from typing import List, Type, Optional
from pydantic.json import pydantic_encoder
from pydantic.dataclasses import dataclass
from pydantic import BaseModel, Field, validator
from tabulate import tabulate
from pprint import pprint
import stringcase
from enum import Enum


from document_issue.project import Project
from document_issue.constants import (
    DIR_TEMPLATES,
    NAME_MD_DOCISSUE_TEMPLATE,
    PATH_REFERENCE_DOCX,
    PATH_REL_IMG,
    NAME_MD_DISCLAIMER_TEMPLATE,
)
from document_issue.enums import scales, paper_sizes, DocSource
from document_issue.basemodel import BaseModel, Field, validator


# TODO:
class FormatConfiguration(BaseModel):
    """configuration options that determine how the output is displayed"""

    date_string_format: str = Field(
        "%d %^b %y",
        description="date display format. refer to: https://www.programiz.com/python-programming/datetime/strptime",
    )
    # description_in_filename: bool = False
    include_author_and_checked_by: bool = Field(
        False,
        description=(
            "Include the initials of the author and checker in the client facing output."
            " Often avoided but some clients (e.g. Canary Wharf) require it."
        ),
    )


description_document_name = """document code. Should be the filename when uploaded
to a CDE. Structured to be machine-readable.""".replace(
    "\n", ""
)
description_name_nomenclature = """denotes what each section of of the document code means
when split on '-' character.
""".replace(
    "\n", ""
)


class Document(Project):
    document_name: str = Field(  # TODO: rename document_name -> document_code
        "06667-MXF-XX-XX-SH-M-20003", description=description_document_name
    )
    document_description: str = Field(
        "Document Description", description="human readable description of the document"
    )
    classification: str = Field(
        "Ac_05",
        description="classification as per Uniclass2015",  # TODO: make this a list...
    )
    name_nomenclature: str = Field(
        "project-originator-volume-level-type-role-number",
        description=description_name_nomenclature,
    )
    size: str = Field(
        "A4", description="paper size of the document", examples=paper_sizes
    )
    scale: str = Field(
        "NTS",
        description='if drawing, give scale, else "not to scale" (NTS)',
        examples=scales,
    )
    doc_source: str = Field(
        "WD",
        description="software used to author the document",
        examples=DocSource._member_names_,
    )

    @validator("name_nomenclature")
    def validate_name_nomenclature(cls, v, values):
        """fix the author to always be Max Fordham LLP"""
        li_name = v.split("-")  # values['document_name'].split('-')
        li_nomenclature = v.split("-")
        len_name = len(li_name)
        len_nomenclature = len(li_nomenclature)
        if len_name != len_nomenclature:
            raise ValueError(
                f"""
            number of sections in document_name == {len_name}
            number of sections in name_nomenclature == {len_nomenclature}
            they must match!"""
            )
        li_nomenclature = [s.strip() for s in li_nomenclature]
        return "-".join(li_nomenclature)


def pydantic_dataclass_to_file(data: Type[dataclass], fpth="pydantic_dataclass.json"):
    """writes a pydantic BaseModel to file"""
    f = open(fpth, "w")
    f.write(json.dumps(data, indent=4, default=pydantic_encoder))
    f.close()
    return fpth


class IssueFormatCodes(Enum):
    """maps IssueFormat codes to string description"""

    cde = "Uploaded to the project common data environment"
    ea = "Sent as Email attachment"
    el = "Sent as Email with a link to file download"
    p = "paper - full size"
    r = "paper - reduced size"


class IssueFormatEnum(str, Enum):
    """in what form was the issue delivered"""

    cde = "cde"
    ea = "ea"
    el = "el"
    p = "p"
    r = "r"


description_author = """
the person who authored the work.""".replace(
    "\n", ""
)
description_checked_by = """
the person who checked the work. 
""".replace(
    "\n", ""
)

COL_WIDTH = 100


class Issue(BaseModel):
    """required information fields that define the metadata of a document issue"""

    revision: str = Field("P01", column_width=COL_WIDTH)
    date: datetime.date = Field(datetime.date(2020, 1, 2), column_width=COL_WIDTH)
    status_code: str = Field("S2", column_width=COL_WIDTH)
    status_description: str = Field(
        "Suitable for information",
        description="this is a BIM field that matches directly with status_code.",
        column_width=150,
    )
    author: Optional[str] = Field(
        "EG", description=description_author, column_width=COL_WIDTH
    )
    checked_by: Optional[str] = Field(
        "CK", description=description_checked_by, column_width=COL_WIDTH
    )
    issue_format: IssueFormatEnum = Field(
        "cde", title="Issue Format", column_width=COL_WIDTH
    )
    issue_notes: str = Field(
        "",
        description="free field where the Engineer can briefly summarise changes since previous issue",
        column_width=300,
    )

    @validator("date", pre=True)
    def _date(cls, v):
        if type(v) == str:
            if "-" in v:
                v = datetime.datetime.strptime(v, "%Y-%m-%d").date()
            else:
                v = datetime.datetime.strptime(v, "%m %b %y").date()
        return v  # TODO: i think this validation step can probs be removed if the code runs differently...


class DocumentIssueBase(Document):
    """metadata to be accompanied by every formal document issue.

    Not all data fields are required for every document type,
    but no document will require additional data fields.
    """

    issue_history: List[Issue] = Field(
        [Issue()],
        format="dataframe",
        layout={"height": "200px"},
    )
    notes: List[str] = Field(["add notes here"])
    originator: str = Field(
        "Max Fordham LLP",
        const=True,
        description="the company the info came from (fixed to be Max Fordham LLP). the name 'originator' comes from BS EN ISO 19650-2",
    )
    format_configuration: FormatConfiguration = FormatConfiguration()

    @validator("notes", pre=True, always=True)
    def make_string(cls, v):
        return [str(n) for n in v]


class DocumentIssue(DocumentIssueBase):  # TODO: rename DocumentIssue
    @property
    def filename(self):
        if self.format_configuration.description_in_filename:
            return self.document_name + "-" + self.document_description.replace(" ", "")
        else:
            return self.document_name

    @property
    def df_issue_history(self):
        li = [i.dict() for i in self.issue_history]
        df = (
            pd.DataFrame(li).sort_values("date", ascending=False).reset_index(drop=True)
        )
        df["date"] = pd.to_datetime(df.date).dt.strftime(
            self.format_configuration.date_string_format
        )
        return df

    @property
    def df_roles(self):
        return pd.DataFrame([i.dict() for i in self.roles]).set_index("name")

    @property
    def df_current_issue(self):
        return pd.DataFrame([self.current_issue.dict()])

    @property
    def df_notes(self):
        return pd.DataFrame.from_dict(
            {"notes": self.notes, "index": list(range(1, len(self.notes) + 1))}
        ).set_index("index")

    @property
    def current_issue(self):
        return self.issue_history[-1]  # Issue(**self.df_issue_history.loc[0].to_dict())

    @property
    def current_issue_long_date(self):
        return self.current_issue.date.strftime("%B %Y")

    @property
    def df_current_issue_header_table(self):
        di = {}
        di["status code"] = self.current_issue.status_code
        di["revision"] = self.current_issue.revision
        di["status description"] = self.current_issue.status_description
        di = {
            **di,
            **dict(
                zip(self.name_nomenclature.split("-"), self.document_name.split("-"))
            ),
        }
        di = {k: [v] for k, v in di.items()}
        return pd.DataFrame.from_dict(di).set_index("status code")

    @property
    def current_status_description(self):
        return self.current_issue.status_description

    @property
    def current_revision(self):
        return self.current_issue.revision


class MarkdownIssue:
    """create structured markdown header from DocumentIssue object"""

    def __init__(
        self,
        dh: DocumentIssue,
        fpth_md_docissue: Optional[pathlib.Path] = None,
        path_rel_img: pathlib.Path = PATH_REL_IMG,
        tomd=False,
        todocx=False,
        fpth_refdocx=PATH_REFERENCE_DOCX,
    ):
        self.dh = dh
        # TODO: make sure this works
        if self.dh.format_configuration.include_author_and_checked_by:
            issue_history_cols = [
                "date",
                "revision",
                "status_code",
                "status_description",
                "issue_notes",
                "author",
                "checked_by",
            ]
        else:
            issue_history_cols = [
                "date",
                "revision",
                "status_code",
                "status_description",
                "issue_notes",
            ]
        self.path_rel_img = path_rel_img
        self.file_loader = FileSystemLoader(DIR_TEMPLATES)
        self.env = Environment(loader=self.file_loader)
        if fpth_md_docissue is None:
            fpth_md_docissue = pathlib.Path(self.dh.filename + ".docissue.md")
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
        if todocx:
            self.tomd = True
        self.todocx = todocx
        self.fpth_refdocx = fpth_refdocx
        self.disclaimer = self._disclaimer()
        if self.tomd:
            self._tomd()
        if self.todocx:
            self._todocx()

    def _disclaimer(self):
        if not self.path_disclaimer_spacer.is_file():
            self.dir_disclaimer_spacer.mkdir(exist_ok=True)
            from document_issue.utils import make_disclaimer_spacer

            make_disclaimer_spacer(self.dir_disclaimer_spacer)
        template = self.env.get_template(NAME_MD_DISCLAIMER_TEMPLATE)
        return template.render(fdirRelImg=self.path_rel_img)

    def _tomd(self):
        if self.fpth_md_docissue is not None:
            f = open(self.fpth_md_docissue, "w")
            f.write(self.md_header)
            f.close()
        else:
            raise ValueError("fpth_md_docissue not given")

    def _todocx(self):
        fpth_md = self.fpth_md_docissue
        fpth_docx = str(pathlib.Path(fpth_md).with_suffix(".docx"))
        self.fpth_docx_header = fpth_docx
        if self.fpth_refdocx.is_file():
            fpth_refdocx = self.fpth_refdocx
            cmd = f"pandoc {fpth_md} -s -f markdown -t docx -o {fpth_docx} --filter=pandoc-docx-pagebreakpy --reference-doc={fpth_refdocx} --columns=6"
        else:
            cmd = f"pandoc {fpth_md} -s -f markdown -t docx -o {fpth_docx} --filter=pandoc-docx-pagebreakpy --columns=6"
        subprocess.run(cmd.split(" "))

    @property
    def md_current_issue_header_table(self):
        cols = [
            f"[{l}]" + "{custom-style='mf_headertitles'}"
            for l in list(self.dh.df_current_issue_header_table.reset_index())
        ]
        vals = [
            f"__{l}__"
            for l in list(self.dh.df_current_issue_header_table.reset_index().loc[0])
        ]
        df = pd.DataFrame.from_dict({"cols": cols, "vals": vals}).T
        md = tabulate(df, showindex=False, tablefmt="grid")
        return [f"        {l}" for l in md.splitlines()]

    @property
    def md_issue_history(self):
        df = self.dh.df_issue_history[self.issue_history_cols]
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
        return self.dh.df_roles.to_markdown()

    @property
    def md_notes(self):
        return self.dh.df_notes.to_markdown()

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
    def md_header(self):
        template = self.env.get_template(NAME_MD_DOCISSUE_TEMPLATE)
        return template.render(
            project_name=self.dh.project_name,
            document_description=self.dh.document_description,
            current_status_description=self.dh.current_status_description,
            author=self.dh.originator,
            current_issue_long_date=self.dh.current_issue_long_date,
            document_name=self.dh.document_name,
            li_current_issue_header_table=self.md_current_issue_header_table,
            md_page_two=self.md_page_two,
        )
