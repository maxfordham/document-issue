import pathlib
import shutil
import pytest

from document_issue.document import Document
from document_issue_io.markdown_issue import MarkdownIssue
from document_issue_io.constants import PATH_REFERENCE_DOCX

from polyfactory.factories.pydantic_factory import ModelFactory

DIR_TESTS = pathlib.Path(__file__).parent
DIR_TESTDATA = DIR_TESTS / "testdata"
FPTH_TEST_DOC_ISSUE = DIR_TESTDATA / "document_issue.json"
FPTH_TEST_DOC_ISSUE_SCHEMA = DIR_TESTDATA / "document_issue.schema.json"


@pytest.fixture(scope="class")
def refresh_dir():
    shutil.rmtree(DIR_TESTDATA, ignore_errors=True)
    DIR_TESTDATA.mkdir(parents=True, exist_ok=True)


class DocumentFactory(ModelFactory[Document]):
    __model__ = Document


@pytest.mark.usefixtures("refresh_dir")
class TestMarkdownIssue:
    def test_create_markdown_issue(self):
        doc = DocumentFactory.build()
        mh = MarkdownIssue(
            doc,
            fpth_md_docissue=DIR_TESTDATA / "test_basic.dh.md",
            tomd=True,
            todocx=True,
            fpth_refdocx=PATH_REFERENCE_DOCX,
        )
        assert pathlib.Path(mh.fpth_md_docissue).is_file()
        assert pathlib.Path(mh.fpth_docx_docissue).is_file()
