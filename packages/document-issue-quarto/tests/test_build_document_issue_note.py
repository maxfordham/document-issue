import os
import shutil
import subprocess

from tests.constants import (
    FDIR_EXAMPLES_DOC_ISSUE_NOTE,
    FDIR_ROOT,
    FDIR_TEST_OUTPUT_DOC_ISSUE_NOTE,
)


def test_install_extension():
    FDIR_EXAMPLE_DATA = FDIR_EXAMPLES_DOC_ISSUE_NOTE / "a4-portrait-note"
    FDIR_TESTDATA = FDIR_TEST_OUTPUT_DOC_ISSUE_NOTE / "a4-portrait-note"
    FDIR_TESTDATA.mkdir(exist_ok=True)
    shutil.copytree(FDIR_EXAMPLE_DATA , FDIR_TESTDATA, dirs_exist_ok=True)
    FDIR_EXTENSION_INSTALL_PTH = FDIR_TESTDATA / "_extensions" / "document-issue-note"
    if FDIR_EXTENSION_INSTALL_PTH.exists():
        shutil.rmtree(FDIR_EXTENSION_INSTALL_PTH)
    os.chdir(FDIR_TESTDATA)
    subprocess.run(["quarto", "add", str(FDIR_ROOT), "--no-prompt"], check=False)
    assert FDIR_EXTENSION_INSTALL_PTH.exists()


def test_build_schedule_a4_portrait():
    FDIR_EXAMPLE_DATA = FDIR_EXAMPLES_DOC_ISSUE_NOTE / "a4-portrait-note"
    FDIR_TESTDATA = FDIR_TEST_OUTPUT_DOC_ISSUE_NOTE / "a4-portrait-note"
    FDIR_TESTDATA.mkdir(exist_ok=True)
    shutil.copytree(FDIR_EXAMPLE_DATA , FDIR_TESTDATA, dirs_exist_ok=True)
    FPTH_OUTPUT = FDIR_TESTDATA / "document.pdf"
    FPTH_OUTPUT.unlink(missing_ok=True)
    os.chdir(FDIR_TESTDATA)
    subprocess.run(["quarto", "add", str(FDIR_ROOT), "--no-prompt"], check=False)
    subprocess.run(
        ["quarto", "render", "document.md", "--to", "document-issue-note-pdf"], check=False,
    )
    assert FPTH_OUTPUT.exists()
    FPTH_LOG = FDIR_TESTDATA / "document.log"
    assert (
        not FPTH_LOG.exists()
    )  # log file should be deleted if Quarto PDF compilation is successful


def test_build_schedule_a3_landscape():
    FDIR_EXAMPLE_DATA = FDIR_EXAMPLES_DOC_ISSUE_NOTE / "a3-landscape-note"
    FDIR_TESTDATA = FDIR_TEST_OUTPUT_DOC_ISSUE_NOTE / "a3-landscape-note"
    FDIR_TESTDATA.mkdir(exist_ok=True)
    shutil.copytree(FDIR_EXAMPLE_DATA , FDIR_TESTDATA, dirs_exist_ok=True)
    FPTH_OUTPUT = FDIR_TESTDATA / "document.pdf"
    FPTH_OUTPUT.unlink(missing_ok=True)
    os.chdir(FDIR_TESTDATA)
    subprocess.run(["quarto", "add", str(FDIR_ROOT), "--no-prompt"], check=False)
    subprocess.run(
        ["quarto", "render", "document.md", "--to", "document-issue-note-pdf"], check=False,
    )
    assert FPTH_OUTPUT.exists()
    FPTH_LOG = FDIR_TESTDATA / "document.log"
    assert (
        not FPTH_LOG.exists()
    )  # log file should be deleted if Quarto PDF compilation is successful
