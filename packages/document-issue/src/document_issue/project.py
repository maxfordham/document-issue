"""
define base characteristics of a Project
"""

import typing as ty
from document_issue.constants import DEFAULT_PROJECT_NUMBER
from document_issue.basemodel import BaseModel, Field
from pydantic import BeforeValidator


def is_job_number_string(s):
    return isinstance(s, str) and "J" in s and len(s) == 5


class ProjectBase(BaseModel):
    project_number: ty.Annotated[
        int,
        BeforeValidator(
            lambda v: int(v.replace("J", "")) if is_job_number_string(v) else v
        ),
    ] = Field(DEFAULT_PROJECT_NUMBER, description="unique number project code")
    project_name: str = Field(
        "In House App Testing", description="should be the same as the WebApp"
    )


class Project(ProjectBase):
    pass


if __name__ == "__main__":
    if __debug__:
        j = Project()
        print(j)
