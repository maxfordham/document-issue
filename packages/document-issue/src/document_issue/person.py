from pydantic import Field
from document_issue.basemodel import BaseModel


class _Initials(BaseModel):
    initials: str = Field(description="initial of the person fulfilling the Role", alias="name")

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
