from document_issue_io.utils import document_issue_md_to_pdf, DocumentIssue
import pathlib
import shutil
from polyfactory.factories.pydantic_factory import ModelFactory


class DocumentIssueFactory(ModelFactory[DocumentIssue]):
    __model__ = DocumentIssue


FDIR = pathlib.Path(__file__).parent / "testoutput" / "test_document_issue_md_to_pdf"
shutil.rmtree(FDIR, ignore_errors=True)
FDIR.mkdir(parents=True, exist_ok=True)
FPTH_MD = FDIR / "test.md"
FPTH_PDF = FPTH_MD.with_suffix(".pdf")

MD = """
# title

1.  One
2.  Two
3.  Three

-   convert this notebook to markdown
-   read `docissue.json`
-   convert using `document_issue_md_to_pdf`

## My Project

| Tables   |      Are      |  Cool |
|----------|:-------------:|------:|
| col 1 is |  left-aligned | $1600 |
| col 2 is |    centered   |   $12 |
| col 3 is | right-aligned |    $1 |
"""


def test_document_issue_md_to_pdf():
    FPTH_MD.write_text(MD)
    doc = DocumentIssueFactory.build()
    document_issue_md_to_pdf(doc, FPTH_MD, FPTH_PDF)
    assert FPTH_PDF.is_file()
