import os
import pathlib
import subprocess
from tests.utils_check_doc_properties import check_quarto_doc_properties


FDIR_ROOT = pathlib.Path(__file__).parent
FDIR_TEST = FDIR_ROOT / "quarto-doc-properties"
FPTH_INPUT = FDIR_TEST / "document.qmd"
FPTH_OUTPUT = FDIR_TEST / "document.pdf"


def test_quarto_doc_properties():
    
    FPTH_OUTPUT.unlink(missing_ok=True)
    os.chdir(FDIR_TEST)
    subprocess.run(["quarto", "render", "document.qmd"])
    assert FPTH_OUTPUT.is_file()
    checked_properties = check_quarto_doc_properties(FPTH_INPUT, FPTH_OUTPUT)




