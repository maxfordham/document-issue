import sys
import pathlib

p = str(
    pathlib.Path(__file__).parent.parent.parent.parent.parent / "document-issue" / "src"
)
sys.path.append(p)
from document_issue.role import Role
from document_issue.project import ProjectBase

from pydantic import BaseModel, Field
import typing as ty

# from


# class ProjectRolePost(BaseModel):
#     project_id: int = Field(description="id of the project")
#     role_id: int = Field(description="id of the role")


# mapping table
class ProjectRole(BaseModel):
    project: ProjectBase
    role: Role = Field()

    class Config:
        orm_mode = True


class ProjectRoleGet(ProjectRole):  # ProjectRole
    project_id: int = Field(description="id of the project")
    role_id: int = Field(description="id of the role")

    class Config:
        orm_mode = True


class ProjectRolesGet(BaseModel):
    project: ProjectBase
    roles: ty.List[Role] = Field()

    class Config:
        orm_mode = True
