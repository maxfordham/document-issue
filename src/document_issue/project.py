"""
define base characteristics of a Project
"""
from document_issue.constants import FNM_EXAMPLE_JOB
from document_issue.basemodel import BaseModel, Field


class Role(BaseModel):
    name: str = Field("JG", description="initial of the person fulfilling the Role")
    role: str = Field("Project Engineer")

    # TODO: add validator to only allow defined roles...


description_roles = """defines who is fulfilling various roles on the project.
currently the there is no validation on the "allowed roles", but in the future 
this should probably link up with the work Dan, Andy and Dean having been doing  
on roles and responsibilities. It is suggested that the __Project Leader__ (or senior partner...)
role should be required on every project, and that only 1no Project Leader can exist 
on a project at a given time. Any document can then inherit this Project Leader field.
[TODO: fix the required roles for a project / integrate with WebApp]{custom-style="mf_green"}
""".replace(
    "\n", ""
)


class Project(BaseModel):
    project_name: str = "In House App Testing"
    project_number: str = FNM_EXAMPLE_JOB
    roles: list[Role] = Field(
        default_factory=lambda: [Role()], description=description_roles
    )


if __name__ == "__main__":
    if __debug__:
        j = Project()
        print(j)
