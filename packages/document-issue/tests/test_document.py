from document_issue.document import Document, FormatConfiguration
from obj_funcs import create_project


def test_Document():
    doc = Document(project=create_project())
    schema = Document.model_json_schema()
    assert doc.document_code == "06667-MXF-XX-XX-SH-M-20003"
    di = doc.model_dump(mode="json")
    assert di["document_code"] == "06667-MXF-XX-XX-SH-M-20003"
    assert schema["properties"]["notes"]["items"]["maxLength"] == 10000
    # assert schema["properties"]["notes"]["items"]["layout"] == {"width": "100%"}


def test_FormatConfiguration():
    fconf = FormatConfiguration(output_author=True)
    check = fconf.output_author
    assert check
