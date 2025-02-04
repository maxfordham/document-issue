"""define base characteristics of a Project
"""

import logging
import typing as ty

from pydantic import (
    AliasChoices,
    BeforeValidator,
    Field,
    model_validator,
)
from typing_extensions import Self

from document_issue.basemodel import BaseModel, Field
from document_issue.constants import DEFAULT_PROJECT_NUMBER


def validate_project_number(v: ty.Union[str, int]) -> int:
    """Validate project number. If it starts with 'J', remove it and convert to int.
    If it is not a number, log a warning and use the default project number.
    """
    try:
        if isinstance(v, str) and v.startswith("J"):
            return int(v.replace("J", ""))
        return int(v)
    except ValueError:
        logging.warning(f"Invalid project number: {v}. Use default.")
        return DEFAULT_PROJECT_NUMBER


class ProjectBase(BaseModel):
    client_name: ty.Optional[str] = Field(
        None,  # TODO: this should probs be required... should also be taken from WebApp.
        validation_alias=AliasChoices(
            "Client Name",
        ),
    )
    project_number: ty.Annotated[
        int,
        BeforeValidator(validate_project_number),
    ] = Field(
        DEFAULT_PROJECT_NUMBER,
        description="unique Max Fordham number project number",
        validation_alias=AliasChoices("Job Number", "job_number"),
    )
    project_code: ty.Optional[str] = Field(
        None,
        description="design team project code (if different from project number)",
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

    @model_validator(mode="after")
    def validate_project_code(self) -> Self:
        if self.project_code is None:
            self.project_code = f"J{self.project_number}"
        return self


class Project(ProjectBase):
    pass


if __name__ == "__main__":
    if __debug__:
        j = Project()
        print(j)
