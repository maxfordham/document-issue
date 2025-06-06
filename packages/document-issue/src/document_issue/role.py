import typing as ty

from pydantic import AliasChoices, Field

from document_issue.basemodel import BaseModel
from document_issue.enums import RoleEnum
from document_issue.person import _Initials


# TODO:
# do you roles need to be editable data fields (with their own table)
# or can they just be enums that get defined globally?
# table
class Role(BaseModel):
    role_name: ty.Union[str, RoleEnum] = Field(
        title="Role",
        description="name of the role",
    )
    role_description: str = Field(
        "",
        title="Role Description",
        description="description of the role",
        json_schema_extra=dict(column_width=300),
    )  # TODO options enum for dynamic dropdown


class DocumentRole(_Initials):
    role_name: RoleEnum = Field(
        validation_alias=AliasChoices("role", "role_name"),
        title="Role",
    )  # NOTE: alias for backwards compatibility with xl DNG
