from document_issue.basemodel import BaseModel, Field
from document_issue.enums import RoleEnum
import typing as ty


# table
class Role(BaseModel):
    role_name: ty.Union[str, RoleEnum] = Field(description="name of the role")
    role_description: str = Field(
        description="description of the role",
        column_width=300,
    )  # TODO options enum for dynamic dropdown
