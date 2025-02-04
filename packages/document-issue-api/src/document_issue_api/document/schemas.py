from document_issue.document import DocumentBase  # , Document, Project, Role
from document_issue.document_issue import DocumentIssue
from document_issue.project import ProjectBase


class DocumentBasePost(DocumentBase):
    """Issue post schema."""

    project_id: int


class DocumentBasePatch(DocumentBase):
    """Issue post schema."""



class DocumentBaseGet(DocumentBasePost):
    """Issue get schema."""

    id: int
    project: ProjectBase


class DocumentIssueGet(DocumentIssue):
    """Issue post schema."""

