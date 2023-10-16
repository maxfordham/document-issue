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


class Issue(BaseModel):
    """required information fields that define the metadata of a document issue"""

    revision: str = Field("P01", json_schema_extra=dict(column_width=COL_WIDTH))
    date: datetime.date = Field(datetime.date(2020, 1, 2), json_schema_extra=dict(column_width=COL_WIDTH))
    status_code: str = Field("S2", json_schema_extra=dict(column_width=COL_WIDTH))
    status_description: str = Field(
        "Suitable for information",
        description="this is a BIM field that matches directly with status_code.",
        json_schema_extra=dict(column_width=150),
    )
    author: ty.Optional[str] = Field(
        "EG", description=description_author, json_schema_extra=dict(column_width=COL_WIDTH)
    )
    checked_by: ty.Optional[str] = Field(
        "CK", description=description_checked_by, json_schema_extra=dict(column_width=COL_WIDTH)
    )
    issue_format: IssueFormatEnum = Field(
        IssueFormatEnum.cde, title="Issue Format", json_schema_extra=dict(column_width=COL_WIDTH)
    )
    issue_notes: str = Field(
        "",
        description="free field where the Engineer can briefly summarise changes since previous issue",
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
