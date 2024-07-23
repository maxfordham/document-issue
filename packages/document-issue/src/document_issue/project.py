"""
define base characteristics of a Project
"""

import logging
import typing as ty
from document_issue.constants import DEFAULT_PROJECT_NUMBER
from document_issue.basemodel import BaseModel, Field
from pydantic import (
    BeforeValidator,
    AliasChoices,
    field_validator,
    Field,
    ValidationInfo,
)


def validate_project_number(v: ty.Union[str, int]) -> int:
    """Validate project number. If it starts with 'J', remove it and convert to int.
    If it is not a number, log a warning and use the default project number."""
    try:
        if isinstance(v, str) and v.startswith("J"):
            return int(v.replace("J", ""))
        else:
            return int(v)
    except ValueError:
        logging.warning(f"Invalid project number: {v}. Use default.")
        return DEFAULT_PROJECT_NUMBER


class ProjectBase(BaseModel):
    client_name: ty.Optional[str] = Field(
        validation_alias=AliasChoices(
            "Client Name",
        )
    )
    project_number: ty.Annotated[
        int,
        BeforeValidator(validate_project_number),
    ] = Field(
        DEFAULT_PROJECT_NUMBER,
        description="unique Max Fordham number project number",
        validation_alias=AliasChoices("Job Number", "job_number"),
    )
    project_code: ty.Union[str, int, None] = Field(
        None,
        description="design team project code",
        validation_alias=AliasChoices("Project Code", "Job Code"),
    )
    project_name: str = Field(
        "In House App Testing",
        description="should be the same as the WebApp",
        validation_alias=AliasChoices(
            "Project Name",
        ),
    )
    project_address: ty.Optional[str] = Field(
        None,
        validation_alias=AliasChoices(
            "Project Address",
        ),
    )

    @field_validator("project_code")
    def validate_project_address(cls, v, info: ValidationInfo):
        if v is None:
            return info.get("project_number")
        else:
            return v


class Project(ProjectBase):
    pass


if __name__ == "__main__":
    if __debug__:
        j = Project()
        print(j)
