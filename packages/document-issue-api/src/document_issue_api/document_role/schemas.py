import typing as ty

from document_issue.basemodel import BaseModel, Field
from document_issue.person import Person
from document_issue.project import ProjectBase
from document_issue.role import Role

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
