from document_issue.project import Project, ProjectBase


class ProjectPost(ProjectBase):
    pass


class ProjectGet(ProjectPost):
    """Project get schema."""

    id: int


class ProjectPatch(ProjectPost):
    """Project patch schema."""

    pass
