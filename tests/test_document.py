from document_issue.document import Document


def test_Document():
    doc = Document()
    assert doc.document_name == "06667-MXF-XX-XX-SH-M-20003"
