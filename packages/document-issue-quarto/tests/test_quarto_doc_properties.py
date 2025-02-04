import os
import shutil
import subprocess

from tests.constants import FDIR_EXAMPLES_DOC_ISSUE_REPORT, FDIR_TEST_OUTPUT
from tests.utils_check_doc_properties import check_quarto_doc_properties


def test_quarto_doc_properties():
    FDIR_EXAMPLE_DATA = FDIR_EXAMPLES_DOC_ISSUE_REPORT / "quarto-doc-properties"
    FDIR_TESTDATA = FDIR_TEST_OUTPUT / "quarto-doc-properties"
    FDIR_TESTDATA.mkdir(exist_ok=True)
    shutil.copytree(FDIR_EXAMPLE_DATA , FDIR_TESTDATA, dirs_exist_ok=True)
    FPTH_INPUT = FDIR_TESTDATA / "document.qmd"
    FPTH_OUTPUT = FDIR_TESTDATA / "document.pdf"
    FPTH_OUTPUT.unlink(missing_ok=True)
    os.chdir(FDIR_TESTDATA)
    subprocess.run(["quarto", "render", "document.qmd"], check=False)
    assert FPTH_OUTPUT.is_file()
    check_quarto_doc_properties(FPTH_INPUT, FPTH_OUTPUT)




