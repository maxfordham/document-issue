import os
import shutil
import pathlib
import subprocess

FDIR_ROOT = pathlib.Path(__file__).parent.parent
FDIR_TESTS = FDIR_ROOT / "tests"
FDIR_TESTDATA = FDIR_TESTS / "testdata"


def test_install_extension():
    FDIR_EXTENSION_INSTALL_PTH = FDIR_TESTDATA / "_extensions" / "document-issue"
    if FDIR_EXTENSION_INSTALL_PTH.exists():
        shutil.rmtree(FDIR_EXTENSION_INSTALL_PTH)
    os.chdir(FDIR_TESTDATA)
    subprocess.run(["quarto", "add", str(FDIR_ROOT), "--no-prompt"])
    assert FDIR_EXTENSION_INSTALL_PTH.exists()


def test_build_schedule():
    FPTH_OUTPUT = FDIR_TESTDATA / "document.pdf"
    FPTH_OUTPUT.unlink(missing_ok=True)
    os.chdir(FDIR_TESTDATA)
    subprocess.run(["quarto", "add", str(FDIR_ROOT), "--no-prompt"])
    subprocess.run(["quarto", "render", "document.md", "--to", "document-issue-pdf"])
    assert FPTH_OUTPUT.exists()
