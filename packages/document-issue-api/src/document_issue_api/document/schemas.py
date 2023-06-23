import sys
import pathlib


from document_issue.document import (
    DocumentBase,
)  # , Document, Project, Role
from document_issue.project import ProjectBase


class DocumentBasePost(DocumentBase):
    """Issue post schema."""

    project_id: int

    class Config:
        orm_mode = True


class DocumentBasePatch(DocumentBase):
    """Issue post schema."""

    pass


class DocumentBaseGet(DocumentBasePost):
    """Issue get schema."""

    project: ProjectBase

    class Config:
        orm_mode = True
