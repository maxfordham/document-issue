from document_issue.basemodel import BaseModel, Field
from document_issue.enums import roles
from document_issue.project import Project


# table
class Role(BaseModel):
    name: str = Field(description="name of the role", examples=roles)
    description: str = Field(
        description="description of the role",
        column_width=300,
    )  # TODO options enum for dynamic dropdown


# table
class Person(BaseModel):
    initials: str = Field("JG", description="initial of the person fulfilling the Role")
    full_name: str = Field(
        "JG", description="initial of the person fulfilling the Role"
    )


# mapping table
class ProjectRole(Role):
    role: Role = Field(
        description="defines the responsibility of the person fulfilling the role on the project"
    )
    people: list[Person] = Field()


description_roles = """defines who is fulfilling various roles and responsibilities
on the project. Some of these roles are required from a QA and quality assurance perspective.
""".replace(
    "\n", ""
)
