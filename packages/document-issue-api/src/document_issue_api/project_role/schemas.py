import typing as ty

from document_issue.basemodel import BaseModel
from document_issue.person import Person
from document_issue.project import ProjectBase
from document_issue.project_role import ProjectRoles
from document_issue.role import Role
from pydantic import Field

# class ProjectRolePost(BaseModel):
#     project_id: int = Field(description="id of the project")
#     role_id: int = Field(description="id of the role")


class PersonGet(Person):
    pass


# mapping table
class ProjectRole(BaseModel):
    project: ProjectBase
    role: Role = Field()
    person: ty.Optional[PersonGet]


class ProjectRoleGet(ProjectRole):  # ProjectRole
    project_id: int = Field(description="id of the project")
    role_id: int = Field(description="id of the role")
    person_id: ty.Optional[int]


class ProjectRolesGet(BaseModel):
    project: ProjectBase
    project_roles: ProjectRoles
