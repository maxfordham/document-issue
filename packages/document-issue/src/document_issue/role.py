from document_issue.basemodel import BaseModel, Field
from document_issue.enums import roles


# table
class Role(BaseModel):
    role_name: str = Field(description="name of the role", examples=roles)
    role_description: str = Field(
        description="description of the role",
        column_width=300,
    )  # TODO options enum for dynamic dropdown

    class Config:
        orm_mode = True


# table
class Person(BaseModel):
    initials: str = Field("JG", description="initial of the person fulfilling the Role")
    full_name: str = Field(
        "JG", description="initial of the person fulfilling the Role"
    )


description_roles = """defines who is fulfilling various roles and responsibilities
on the project. Some of these roles are required from a QA and quality assurance perspective.
""".replace(
    "\n", ""
)
