from document_issue.document_new import Document
from document_issue.project import ProjectBase
from obj_funcs import create_project_base


def test_Document():
    doc = Document(project=create_project_base())
    assert doc.document_code == "06667-MXF-XX-XX-SH-M-20003"
