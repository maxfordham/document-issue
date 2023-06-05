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
from document_issue.enums import IssueFormatEnum, IssueStatusEnum

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


class DocumentBase(BaseModel):
    name_nomenclature: str = Field(
        "project-originator-volume-level-type-role-number",
        description=description_name_nomenclature,
    )
    document_name: str = Field(  # TODO: rename document_name -> document_code
        "06667-MXF-XX-XX-SH-M-20003", description=description_document_name
    )
    document_description: str = Field(
        "Document Description", description="human readable description of the document"
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
    notes: List[str] = Field(["add notes here"])
    originator: str = Field(
        "Max Fordham LLP",
        const=True,
        description="the company the info came from (fixed to be Max Fordham LLP). the name 'originator' comes from BS EN ISO 19650-2",
    )  # TODO: remove. should be picked up in classification data.
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


class Document(DocumentBase):
    project: Project = Field(..., description="the project this document belongs to")
    classification: Classification = Field(None)
    issue_history: ty.List[Issue] = Field(
        format="dataframe",
        layout={"height": "200px"},
    )
