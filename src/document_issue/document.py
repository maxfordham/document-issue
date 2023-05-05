# document
"""
object model for defining the fields required for a structured document (TODO: add iso reference here)
"""
import shutil
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

# from ipyword.constants import FPTH_DISCLAIMER_SPACER
FPTH_DISCLAIMER_SPACER = (
    "/mnt/c/engDev/git_mf/ipyword/ipyword/images/disclaimer_spacer.png"
)
PATH_DISCLAIMER_SPACER = pathlib.Path(FPTH_DISCLAIMER_SPACER)

from document_issue.project import Project
from document_issue.utils import read_json
from document_issue.constants import (
    PATH_DISCLAIMER,
    DIR_TEMPLATES,
    NAME_MD_HEADER_TEMPLATE,
    PATH_REFERENCE_DOCX,
    PATH_REL_IMG,
    NAME_MD_DISCLAIMER_TEMPLATE,
)

from document_issue.basemodel import BaseModel, Field, validator

# TODO:
class FormatConfiguration(BaseModel):
    date_string_format: str = (
        "%d %^b %y"  # https://www.programiz.com/python-programming/datetime/strptime
    )
    description_in_filename: bool = False
    include_author_and_checked_by: bool = False  # TODO: implement


class Document(Project):
    document_name: str = "06667-MXF-XX-XX-SH-M-20003"
    document_description: str = "Document Description"  # e.g. Light Fitting Schedule
    classification: str = Field(
        "Ac_05", description="classification as per Uniclass2015"
    )
    name_nomenclature: str = "project code-originator-volume-level-type-role-number"
    size: str = Field("A4", description="paper size of the document")
    scale: str = Field(
        "NTS", description='if drawing, give scale, else "not to scale" (NTS)'
    )
    doc_source: str = Field("WD", description="software used to author the document")
    date_string_format: str = "%d %^b %y"
    # ^ https://www.programiz.com/python-programming/datetime/strptime
    description_in_filename: bool = False
    include_author_and_checked_by: bool = False  # TODO: implement

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





@dataclass
class IssueFormatCodes:
    """maps IssueFormat codes to string description"""

    cde: str = "Uploaded to the project common data environment"
    ea: str = "Sent as Email attachment"
    el: str = "Sent as Email with a link to file download"
    p: str = "paper - full size"
    r: str = "paper - reduced size"


class IssueFormatEnum(str, Enum):
    cde = "cde"
    ea = "ea"
    el = "el"
    p = "p"
    r = "r"


description_author = """
the person who authored the work. 
this is an optional field as for many info types listing a single author is not appropriate. 
_could change the type to be either a single author or a list of authors..._
this field has been explicitly requested by Canary Wharf."""
description_checked_by = """
the person who checked the work. 
this is an optional field as for many info types listing a single checked_by is not appropriate. 
_could change the type to be either a single author or a list of authors..._
this field has been explicitly requested by Canary Wharf.
it is most appropriate for drawings - less so for Spec. """


class Issue(BaseModel):
    """required information fields that define the metadata of a document issue"""

    revision: str = "P01"
    date: datetime.date = datetime.date(2020, 1, 2)
    status_code: str = "S2"
    status_description: str = Field(
        "Suitable for information",
        description="this is a BIM field that matches directly with status_code. TODO: add validation",
    )
    author: Optional[str] = Field("EG", description=description_author)
    checked_by: Optional[str] = Field("CK", description=description_checked_by)
    issue_format: IssueFormatEnum = Field(
        "cde", description="in what form was the issue delivered"
    )
    issue_notes: str = Field(
        "",
        description="free field where the Engineer can briefly summarise changes since previous issue",
    )

    @validator("date", pre=True)
    def _date(cls, v):
        if type(v) == str:
            if "-" in v:
                v = datetime.datetime.strptime(v, "%Y-%m-%d").date()
            else:
                v = datetime.datetime.strptime(v, "%m %b %y").date()
        return v  # TODO: i think this validation step can probs be removed if the code runs differently...


class DocumentHeaderBase(Document):
    """metadata to be accompanied by every formal document issue.

    __Aspiration__: not all data fields are required for every document type,
    but no document will require additional data fields.

    __Note__: The parameter names are stored in the background as "camelCase"
    but are output as "sentence case" (all lower case). This is configurable and simple to change.
    """

    issue_history: List[Issue] = Field(default_factory=lambda: [Issue()])
    notes: List[str] = Field(default_factory=lambda: ["add notes here"])
    originator: str = Field(
        "Max Fordham LLP",
        const=True,
        description="the company the info came from (fixed to be Max Fordham LLP). the name 'originator' comes from BS EN ISO 19650-2",
    )
    format_configuration: FormatConfiguration = FormatConfiguration()

    @validator("notes", pre=True, always=True)
    def make_string(cls, v):
        return [str(n) for n in v]


class DocumentHeader(DocumentHeaderBase):
    @property
    def filename(self):
        if self.format_configuration.description_in_filename:
            return self.document_name + "-" + self.document_description.replace(" ", "")
        else:
            return self.document_name

    @property
    def df_issue_history(self):
        di = [i.dict() for i in self.issue_history]
        df = (
            pd.DataFrame.from_dict(di)
            .sort_values("date", ascending=False)
            .reset_index(drop=True)
        )
        df["date"] = pd.to_datetime(df.date).dt.strftime(
            self.format_configuration.date_string_format
        )
        return df

    @property
    def df_roles(self):
        return pd.DataFrame.from_dict([i.dict() for i in self.roles]).set_index("name")

    @property
    def df_current_issue(self):
        return pd.DataFrame.from_dict([self.current_issue.dict()])

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


class MarkdownHeader:
    """create structured markdown header from DocumentHeader object"""

    def __init__(
        self,
        dh: DocumentHeader,
        fpth_md_header: pathlib.Path = pathlib.Path("."),
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
        self.fpth_md_header = fpth_md_header
        self.path_md_header = fpth_md_header.parent
        self.dir_disclaimer_spacer = (self.path_md_header / self.path_rel_img).resolve()
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
            shutil.copyfile(
                PATH_DISCLAIMER_SPACER,
                (self.dir_disclaimer_spacer / PATH_DISCLAIMER_SPACER.name),
            )
        template = self.env.get_template(NAME_MD_DISCLAIMER_TEMPLATE)
        return template.render(fdirRelImg=self.path_rel_img)

    def _tomd(self):
        if self.fpth_md_header is not None:
            f = open(self.fpth_md_header, "w")
            f.write(self.md_header)
            f.close()
        else:
            raise ValueError("fpth_md_header not given")

    def _todocx(self):
        fpth_md = self.fpth_md_header
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
        template = self.env.get_template(NAME_MD_HEADER_TEMPLATE)
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

