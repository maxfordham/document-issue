import typing as ty
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
from document_issue.enums import IssueFormatEnum  # , IssueStatusEnum

from document_issue.project import Project
from document_issue.constants import (
    DIR_TEMPLATES,
    NAME_MD_DOCISSUE_TEMPLATE,
    PATH_REFERENCE_DOCX,
    PATH_REL_IMG,
    NAME_MD_DISCLAIMER_TEMPLATE,
)
from document_issue.enums import ScalesEnum, PaperSizeEnum, DocSource
from document_issue.basemodel import BaseModel, Field, validator
from document_issue.constants import COL_WIDTH
from document_issue.issue import Issue


class Classification(BaseModel):
    pass


class FormatConfiguration(BaseModel):
    """configuration options that determine how the output is displayed"""

    date_string_format: str = Field(
        "%d %^b %y",
        description="date display format. refer to: https://www.programiz.com/python-programming/datetime/strptime",
    )
    output_author: bool = Field(
        False,
        description=(
            "Include the initials of the author in the client facing output."
            " Often avoided but some clients require it."
        ),
    )
    output_checked_by: bool = Field(
        False,
        description=(
            "Include the initials of the checker in the client facing output."
            " Often avoided but some clients require it."
        ),
    )


description_document_code = """document code. Should be the filename when uploaded
to a CDE. Structured to be machine-readable.""".replace(
    "\n", ""
)
description_name_nomenclature = """denotes what each section of of the document code means
when split on '-' character.
""".replace(
    "\n", ""
)


class DocumentBase(FormatConfiguration):
    name_nomenclature: str = Field(
        "project-originator-volume-level-type-role-number",
        description=description_name_nomenclature,
    )
    document_code: str = Field(
        "06667-MXF-XX-XX-SH-M-20003", description=description_document_code
    )
    document_description: str = Field(
        "Document Description", description="human readable description of the document"
    )
    document_source: str = Field(
        "WD",
        description="software used to author the document",
        examples=DocSource._member_names_,
    )
    # document_filetype: str = Field() # include this?
    paper_size: str = Field(
        "A4", description="paper size of the document", examples=PaperSizeEnum
    )
    scale: str = Field(
        "NTS",
        description='if drawing, give scale, else "not to scale" (NTS)',
        examples=ScalesEnum,
    )

    notes: List[str] = Field(["add notes here"])
    originator: str = Field(
        "Max Fordham LLP",
        const=True,
        description="the company the info came from (fixed to be Max Fordham LLP). the name 'originator' comes from BS EN ISO 19650-2",
    )  # TODO: remove. should be picked up in classification data.

    @validator("name_nomenclature")
    def validate_name_nomenclature(cls, v, values):
        """fix the author to always be Max Fordham LLP"""
        li_name = v.split("-")  # values['document_code'].split('-')
        li_nomenclature = v.split("-")
        len_name = len(li_name)
        len_nomenclature = len(li_nomenclature)
        if len_name != len_nomenclature:
            raise ValueError(
                f"""
            number of sections in document_code == {len_name}
            number of sections in name_nomenclature == {len_nomenclature}
            they must match!"""
            )
        li_nomenclature = [s.strip() for s in li_nomenclature]
        return "-".join(li_nomenclature)


class Document(DocumentBase):
    project: Project = Field(..., description="the project this document belongs to")
    classification: Classification = Field(None)  # TODO: add classification
    issue_history: ty.List[Issue] = Field(
        [],
        description="list of issues",
        format="dataframe",
        layout={"height": "200px"},
    )

    @property
    def filename(self):
        return self.document_code

    @property
    def df_issue_history(self):
        li = [i.dict() for i in self.issue_history]
        df = (
            pd.DataFrame(li).sort_values("date", ascending=False).reset_index(drop=True)
        )
        df["date"] = pd.to_datetime(df.date).dt.strftime(self.date_string_format)
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
                zip(self.name_nomenclature.split("-"), self.document_code.split("-"))
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
