"""
define base characteristics of a Project
"""

import logging
import typing as ty
from document_issue.constants import DEFAULT_PROJECT_NUMBER
from document_issue.basemodel import BaseModel, Field
from pydantic import BeforeValidator


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
    client_name: str
    project_number: ty.Annotated[
        int,
        BeforeValidator(validate_project_number),
    ] = Field(DEFAULT_PROJECT_NUMBER, description="unique number project code")
    project_name: str = Field(
        "In House App Testing", description="should be the same as the WebApp"
    )
    project_address: ty.Optional[str] = Field(None)


class Project(ProjectBase):
    pass


if __name__ == "__main__":
    if __debug__:
        j = Project()
        print(j)
