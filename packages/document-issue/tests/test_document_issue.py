from document_issue.document_issue import Issue

def test_Issue():
    issue = Issue()
    assert issue.revision == "P01"
    di = issue.model_dump(mode="json")
    assert di["revision"] == "P01"
    