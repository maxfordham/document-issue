from document_issue.project import ProjectBase


class ProjectPost(ProjectBase):
    pass


class ProjectGet(ProjectPost):
    """Project get schema."""

    id: int


class ProjectPatch(ProjectPost):
    """Project patch schema."""

