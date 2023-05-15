"""
define base characteristics of a Project
"""
from document_issue.constants import FNM_EXAMPLE_JOB
from document_issue.basemodel import BaseModel, Field
from document_issue.enums import roles


class Role(BaseModel):
    name: str = Field("JG", description="initial of the person fulfilling the Role")
    role: str = Field("Project Engineer", column_width=300, examples=roles)

    # TODO: add validator to only allow defined roles...


description_roles = """defines who is fulfilling various roles and responsibilities
on the project. Some of these roles are required from a QA and quality assurance perspective.
""".replace(
    "\n", ""
)


class Project(BaseModel):
    project_name: str = Field(
        "In House App Testing", description="should be the same as the WebApp"
    )
    project_number: str = Field(
        FNM_EXAMPLE_JOB, description="MXF unique number prefixed by J"
    )
    roles: list[Role] = Field(
        [Role()],
        description=description_roles,
        format="dataframe",
        layout={"height": "200px"},
    )


if __name__ == "__main__":
    if __debug__:
        j = Project()
        print(j)
