import sys
import pathlib

p = str(
    pathlib.Path(__file__).parent.parent.parent.parent.parent / "document-issue" / "src"
)
sys.path.append(p)

from document_issue.document import Issue  # , Document, Project, Role


class IssueBasePost(Issue):
    """Issue post schema."""

    pass
