from document_issue.project import Project, ProjectBase


class ProjectPost(ProjectBase):
    """Project post schema."""

    class Config:
        orm_mode = True


class ProjectGet(ProjectPost):
    """Project get schema."""

    id: int


class ProjectPatch(ProjectPost):
    """Project patch schema."""

    pass
