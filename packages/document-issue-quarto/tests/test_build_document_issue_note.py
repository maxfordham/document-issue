import os
import shutil
import pathlib
import subprocess

FDIR_ROOT = pathlib.Path(__file__).parent.parent
FDIR_TESTS = FDIR_ROOT / "tests" / "test-document-issue-note"


def test_install_extension():
    FDIR_TESTDATA = FDIR_TESTS / "a4-portrait"
    FDIR_EXTENSION_INSTALL_PTH = FDIR_TESTDATA / "_extensions" / "document-issue-note"
    if FDIR_EXTENSION_INSTALL_PTH.exists():
        shutil.rmtree(FDIR_EXTENSION_INSTALL_PTH)
    os.chdir(FDIR_TESTDATA)
    subprocess.run(["quarto", "add", str(FDIR_ROOT), "--no-prompt"])
    assert FDIR_EXTENSION_INSTALL_PTH.exists()


def test_build_schedule_a4_portrait():
    FDIR_TESTDATA = FDIR_TESTS / "a4-portrait"
    FPTH_OUTPUT = FDIR_TESTDATA / "document.pdf"
    FPTH_OUTPUT.unlink(missing_ok=True)
    os.chdir(FDIR_TESTDATA)
    subprocess.run(["quarto", "add", str(FDIR_ROOT), "--no-prompt"])
    subprocess.run(
        ["quarto", "render", "document.md", "--to", "document-issue-note-pdf"]
    )
    assert FPTH_OUTPUT.exists()
    FPTH_LOG = FDIR_TESTDATA / "document.log"
    assert (
        not FPTH_LOG.exists()
    )  # log file should be deleted if Quarto PDF compilation is successful


def test_build_schedule_a3_landscape():
    FDIR_TESTDATA = FDIR_TESTS / "a3-landscape"
    FPTH_OUTPUT = FDIR_TESTDATA / "document.pdf"
    FPTH_OUTPUT.unlink(missing_ok=True)
    os.chdir(FDIR_TESTDATA)
    subprocess.run(["quarto", "add", str(FDIR_ROOT), "--no-prompt"])
    subprocess.run(
        ["quarto", "render", "document.md", "--to", "document-issue-note-pdf"]
    )
    assert FPTH_OUTPUT.exists()
    FPTH_LOG = FDIR_TESTDATA / "document.log"
    assert (
        not FPTH_LOG.exists()
    )  # log file should be deleted if Quarto PDF compilation is successful
