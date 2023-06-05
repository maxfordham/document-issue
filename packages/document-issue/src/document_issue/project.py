"""
define base characteristics of a Project
"""
from document_issue.constants import DEFAULT_PROJECT_NUMBER
from document_issue.basemodel import BaseModel, Field
from document_issue.enums import roles
from document_issue.role import Role


description_roles = """defines who is fulfilling various roles and responsibilities
on the project. Some of these roles are required from a QA and quality assurance perspective.
""".replace(
    "\n", ""
)


class ProjectBase(BaseModel):
    project_name: str = Field(
        "In House App Testing", description="should be the same as the WebApp"
    )
    project_number: int = Field(
        DEFAULT_PROJECT_NUMBER, description="unique number project code"
    )

    class Config:
        orm_mode = True


class Project(ProjectBase):
    roles: list[Role] = Field(
        ...,
        description=description_roles,
        format="dataframe",
        layout={"height": "200px"},
    )


if __name__ == "__main__":
    if __debug__:
        j = Project()
        print(j)
