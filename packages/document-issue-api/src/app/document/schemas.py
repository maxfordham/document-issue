import sys
import pathlib

p = str(
    pathlib.Path(__file__).parent.parent.parent.parent.parent / "document-issue" / "src"
)
sys.path.append(p)

from document_issue.document_new import (
    DocumentBase,
)  # , Document, Project, Role
from document_issue.project import ProjectBase


class DocumentBasePost(DocumentBase):
    """Issue post schema."""

    project_id: int

    class Config:
        orm_mode = True


class DocumentBaseGet(DocumentBasePost):
    """Issue get schema."""

    project: ProjectBase

    class Config:
        orm_mode = True
