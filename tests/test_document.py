from document_issue.document import Document, MarkdownIssue, DocumentIssue


def test_Document():
    doc = Document()
    assert doc.document_name == "06667-MXF-XX-XX-SH-M-20003"


def test_MarkdownIssue():
    di = DocumentIssue()
    di.issue_history[0].issue_notes = (
        "a long a wordy sentence to test the line"
        " wrap in the docx when the text is too long"
    )
    mi = MarkdownIssue(di, todocx=True)
