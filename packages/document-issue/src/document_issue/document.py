import typing as ty
from typing_extensions import Literal
from pydantic import RootModel, field_validator, Field, model_validator

from document_issue.project import ProjectBase
from document_issue.enums import ScalesEnum, PaperSizeEnum, DocSource
from document_issue.basemodel import BaseModel, Field
from document_issue.issue import Issue
from document_issue.project_role import ProjectRoles


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
    include_author_and_checked_by: bool = (
        None  # TODO: for migration only. remove in future.
    )

    @model_validator(mode="after")  # TODO: for migration only. remove in future.
    def check_include_author_and_checked_by(self) -> "UserModel":
        v = self.include_author_and_checked_by
        if v is not None:
            self.output_author = v
            self.output_checked_by = v
        return self


description_document_code = """document code. Should be the filename when uploaded
to a CDE. Structured to be machine-readable.""".replace(
    "\n", ""
)
description_name_nomenclature = """denotes what each section of of the document code means
when split on '-' character.
""".replace(
    "\n", ""
)


class Notes(RootModel):
    root: str = Field(json_schema_extra=dict(layout={"width": "100%"}))


class DocumentBase(BaseModel):
    name_nomenclature: str = Field(
        "project-originator-volume-level-type-role-number",
        description=description_name_nomenclature,
    )
    document_code: str = Field(
        "06667-MXF-XX-XX-SH-M-20003",
        description=description_document_code,
        alias="document_name",
    )
    document_description: str = Field(
        "Document Description", description="human readable description of the document"
    )
    document_source: str = Field(  # TODO: rename `document_source`
        "WD",
        description="software used to author the document",
        examples=DocSource._member_names_,
        alias="doc_source",
    )
    # document_filetype: str = Field() # include this?
    paper_size: ty.Union[str, PaperSizeEnum] = Field(
        "A4", description="paper size of the document", alias="size"
    )
    scale: ty.Union[str, ScalesEnum] = Field(
        "nts",
        description='if drawing, give scale, else "not to scale" (NTS)',
    )
    originator: Literal["Max Fordham LLP"] = Field(
        "Max Fordham LLP",
        description="the company the info came from (fixed to be Max Fordham LLP). the name 'originator' comes from BS EN ISO 19650-2",
        json_schema_extra=dict(type="string", disabled=True),
    )  # TODO: remove. should be picked up in classification data.
    notes: ty.List[str] = Field(["add notes here"])

    @field_validator("name_nomenclature")
    @classmethod
    def validate_name_nomenclature(cls, v):
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
    format_configuration: FormatConfiguration = FormatConfiguration()
