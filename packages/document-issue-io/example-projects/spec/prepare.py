import pathlib
from document_issue.document_issue import DocumentIssue
from document_issue_io.markdown_document_issue import MarkdownDocumentIssue

fdir = pathlib.Path(__file__).parent
document_issue = DocumentIssue.model_validate_json(
    (fdir / "_document_issue.json").read_text()
)
markdown_issue = MarkdownDocumentIssue(document_issue=document_issue)

fpths = fdir.glob("*.md")
fpth_out = fdir / "issue.md"  #
fpth_out.unlink(missing_ok=True)
markdown = MarkdownDocumentIssue(document_issue).md_docissue
li_md = [markdown] + [f.read_text() for f in fpths]

fpth_out.write_text("\n\n".join(li_md))
