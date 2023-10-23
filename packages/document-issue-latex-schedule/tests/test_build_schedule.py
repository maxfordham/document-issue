import os
import pathlib
import subprocess

FDIR_TESTS = pathlib.Path(__file__).parent
FDIR_TESTDATA = FDIR_TESTS / "testdata"

def test_build_schedule():
    FDIR_OUTPUT = FDIR_TESTDATA / "document.pdf"
    FDIR_OUTPUT.unlink(missing_ok=True)
    os.chdir(FDIR_TESTDATA)
    subprocess.run(["quarto", "render", "document.md", "--to", "pdf"])
    assert FDIR_OUTPUT.exists()