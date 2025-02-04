import datetime
import typing as ty

from pydantic import Field, field_validator, model_validator

from document_issue.basemodel import BaseModel
from document_issue.constants import COL_WIDTH
from document_issue.enums import IssueFormatEnum, StatusRevisionEnum

description_author = "the person who authored the work."
description_checked_by = "the person who checked the work."

# TODO: who issued to?


class Issue(BaseModel):
    """required information fields that define the metadata of a document issue"""

    revision_number: int = Field(1, json_schema_extra=dict(column_width=1))
    date: datetime.date = Field(
        datetime.date(2020, 1, 2),
        title="Date",
        json_schema_extra=dict(column_width=COL_WIDTH),
    )
    status_revision: StatusRevisionEnum = Field(
        StatusRevisionEnum.S0_P,
        title="Status Revision Selector",
        json_schema_extra=dict(column_width=1),
    )
    revision: str = Field(
        "",
        title="Rev",
        json_schema_extra=dict(column_width=COL_WIDTH, disabled=True),
    )
    status_code: str = Field(
        "S2",
        title="Status",
        json_schema_extra=dict(column_width=COL_WIDTH, disabled=True),
    )
    status_description: str = Field(
        "Suitable for information",
        title="Description",
        description="this is a BIM field that matches directly with status_code.",
        json_schema_extra=dict(column_width=150, disabled=True),
    )
    author: ty.Optional[str] = Field(
        "EG",
        title="Author",
        description=description_author,
        max_length=5,
        json_schema_extra=dict(column_width=COL_WIDTH),
    )
    checked_by: ty.Optional[str] = Field(
        "CK",
        title="Checker",
        max_length=5,
        description=description_checked_by,
        json_schema_extra=dict(column_width=COL_WIDTH),
    )
    issue_format: IssueFormatEnum = Field(
        IssueFormatEnum.cde,
        title="Issue Format",
        json_schema_extra=dict(column_width=COL_WIDTH),
    )
    issue_notes: str = Field(  # TODO: issue_note ?
        "",
        title="Issue Notes",
        description=(
            "free field where the Engineer can briefly summarise changes/progress."
        ),
        max_length=10000,
        json_schema_extra=dict(column_width=300),
    )

    @property
    def issue_id(self) -> str:
        return f"{self.date.strftime('%Y%m%d')}-{self.status_code}"

    @field_validator("date", mode="before")
    @classmethod
    def _date(cls, v):
        if type(v) == str:
            if "-" in v:
                v = datetime.datetime.strptime(v, "%Y-%m-%d").date()
            else:
                v = datetime.datetime.strptime(v, "%m %b %y").date()
        return v  # TODO: i think this validation step can probs be removed if the code runs differently...

    @field_validator("issue_format", mode="before")
    @classmethod
    def _issue_format(cls, v):
        if v in list(IssueFormatEnum.__members__.keys()):
            return getattr(IssueFormatEnum, v)
        return v

    @model_validator(mode="after")
    def update_status_revision_fields(self) -> "Issue":
        status_revision = (
            lambda sr: sr.value if isinstance(sr, StatusRevisionEnum) else sr
        )(self.status_revision)
        (
            self.status_code,
            status_description,
            revision_code,
            revision_description,
            description,
        ) = status_revision.split(" - ")
        self.revision = f"{revision_code}{str(self.revision_number).zfill(2)}"
        self.status_description = description
        return self
