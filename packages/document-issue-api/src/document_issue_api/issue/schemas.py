from document_issue.issue import Issue  # , Document, Project, Role


class IssueBasePost(Issue):
    """Issue post schema."""

    class Config:
        use_enum_values = True
