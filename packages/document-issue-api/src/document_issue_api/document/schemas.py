from document_issue.document import DocumentBase, DocumentIssue  # , Document, Project, Role
from document_issue.project import ProjectBase
from document_issue.project_role import ProjectRoles


class DocumentBasePost(DocumentBase):
    """Issue post schema."""

    project_id: int


class DocumentBasePatch(DocumentBase):
    """Issue post schema."""

    pass


class DocumentBaseGet(DocumentBasePost):
    """Issue get schema."""

    project: ProjectBase


class DocumentIssueGet(DocumentIssue):
    """Issue post schema."""

    pass
