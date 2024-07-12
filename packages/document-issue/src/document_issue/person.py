from pydantic import Field, field_validator
from document_issue.basemodel import BaseModel


class _Initials(BaseModel):
    initials: str = Field(
        alias="name",
        title="Initials",
        description="initial of the person fulfilling the Role",
        max_length=5,
    )

    @field_validator("initials")
    def initials_validator(cls, v):
        if len(v) > 5:
            v = v[:5]
        return v  # TODO: remove this when deployed via an app. This is a temp fix while still using excel


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
