from document_issue.basemodel import BaseModel, Field, validator
from document_issue.enums import IssueFormatEnum
from document_issue.constants import COL_WIDTH
import datetime
import typing as ty
from pydantic import field_validator


description_author = """
the person who authored the work.""".replace(
    "\n", ""
)
description_checked_by = """
the person who checked the work. 
""".replace(
    "\n", ""
)

# TODO: who issued to?


class Issue(BaseModel):
    """required information fields that define the metadata of a document issue"""

    revision: str = Field(
        "P01", title="Rev", json_schema_extra=dict(column_width=COL_WIDTH)
    )
    date: datetime.date = Field(
        datetime.date(2020, 1, 2),
        title="Date",
        json_schema_extra=dict(column_width=COL_WIDTH),
    )
    status_code: str = Field(
        "S2", title="Status", json_schema_extra=dict(column_width=COL_WIDTH)
    )
    status_description: str = Field(
        "Suitable for information",
        title="Description",
        description="this is a BIM field that matches directly with status_code.",
        json_schema_extra=dict(column_width=150),
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
            "free field where the Engineer can briefly summarise changes since previous"
            " issue"
        ),
        max_length=1e8,
        json_schema_extra=dict(column_width=300),
    )

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
        else:
            return v
