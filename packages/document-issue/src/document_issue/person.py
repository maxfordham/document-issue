from pydantic import BaseModel, Field


# table
class Person(BaseModel):
    initials: str = Field("JG", description="initial of the person fulfilling the Role")
    full_name: str = Field(
        "JG", description="initial of the person fulfilling the Role"
    )


# ----------------------------------------------------
# NOTE: not required, this is more like a persons
# role in the company, covered by Dan's databases.
# ----------------------------------------------------
# class PersonRole(BaseModel):
#     person: Person
#     role: Role
#
#     class Config:
#         orm_mode = True
