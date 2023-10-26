from document_issue.document import Document
from obj_funcs import create_project


def test_Document():
    doc = Document(project=create_project())
    assert doc.document_code == "06667-MXF-XX-XX-SH-M-20003"
