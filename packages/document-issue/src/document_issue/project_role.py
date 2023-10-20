from document_issue.role import Role
from document_issue.person import Person
from document_issue.basemodel import BaseModel, Field
from pydantic import RootModel
import typing as ty

description_roles = """defines who is fulfilling various roles and responsibilities
on the project. Some of these roles are required from a QA and quality assurance perspective.
""".replace(
    "\n", ""
)


class PersonRole(BaseModel):
    role: Role
    person: ty.Optional[Person]


class ProjectRoles(RootModel):
    root: list[PersonRole] = Field(
        [],
        description=description_roles,
    )
