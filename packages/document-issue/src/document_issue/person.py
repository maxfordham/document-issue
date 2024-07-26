from pydantic import Field
from document_issue.basemodel import BaseModel
from typing_extensions import Annotated
from pydantic import BaseModel, AliasChoices
from pydantic.functional_validators import BeforeValidator


def reduce_chars(v: str) -> str:
    if len(v) > 5:
        v = v[:5]
    return v


class _Initials(BaseModel):
    initials: Annotated[str, BeforeValidator(reduce_chars)] = Field(
        validation_alias=AliasChoices("initials", "name"),
        title="Initials",
        description="initial of the person fulfilling the Role",
        max_length=5,
    )


# table
class Person(_Initials):
    full_name: str = Field(description="full name of the person fulfilling the Role")


# ----------------------------------------------------
# NOTE: not required, this is more like a persons
# role in the company, covered by Dan's databases.
# ----------------------------------------------------
# class PersonRole(BaseModel):
#     person: Person
#     role: Role
