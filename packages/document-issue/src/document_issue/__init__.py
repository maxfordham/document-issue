from document_issue.document import Document
from document_issue.document_issue import DocumentIssue
from document_issue.issue import Issue

__all__ = [
    "Document",
    "DocumentIssue",
    "Issue",
]


def demo_document_issue():
    from document_issue.enums import RoleEnum, StatusRevisionEnum
    from document_issue.role import DocumentRole

    issue = Issue(status_revision=StatusRevisionEnum.A4_C)
    document_issue = DocumentIssue(
        document_role=[DocumentRole(role_name=RoleEnum.director, name="DR")],
        issue_history=[issue],
        notes=[
            "This is a note",
            "This is another note",
            ("This is a very long note which states something important about the document issue"),
        ],
    )
    document_issue.project_name = "Rotunda Refurbishment"
    document_issue.client_name = "Max Fordham LLP Partnership"
    document_issue.project_number = "J4321"
    document_issue.document_role[0].initials = "OH"
    document_issue.document_role[0].role_name = "Director in Charge"
    document_issue.document_code = "06667-MXF-XX-XX-SH-M-20003"
    document_issue.document_description = "A description of a Max Fordham\nProject can split\nmultiple lines"  # We can override where the new lines go with \n
    document_issue.name_nomenclature = "project-originator-volume-level-type-role-number"
    return document_issue
