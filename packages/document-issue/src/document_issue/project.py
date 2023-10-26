"""
define base characteristics of a Project
"""
from document_issue.constants import DEFAULT_PROJECT_NUMBER
from document_issue.basemodel import BaseModel, Field


class ProjectBase(BaseModel):
    project_name: str = Field(
        "In House App Testing", description="should be the same as the WebApp"
    )
    project_number: int = Field(
        DEFAULT_PROJECT_NUMBER, description="unique number project code"
    )


class Project(ProjectBase):
    pass


if __name__ == "__main__":
    if __debug__:
        j = Project()
        print(j)
