from document_issue.issue import Issue  # , Document, Project, Role


class IssueBasePost(Issue):
    """Issue post schema."""


class IssueBasePatch(Issue):
    """Issue patch schema."""


class IssueBaseGet(Issue):
    """Issue get schema."""

    id: int
