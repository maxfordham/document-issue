import sys
import pathlib

from document_issue.issue import Issue  # , Document, Project, Role


class IssueBasePost(Issue):
    """Issue post schema."""

    class Config:
        orm_mode = True
        use_enum_values = True
