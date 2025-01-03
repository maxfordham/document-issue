import os
import shutil
import pathlib
import subprocess
import pytest
from tests.utils_check_doc_properties import check_quarto_doc_properties

FDIR_ROOT = pathlib.Path(__file__).parent.parent
FDIR_TESTS = FDIR_ROOT / "tests" / "test-document-issue-report"

# TODO: 
# move examples to examples dir in root and setup to work with the documentation workflow.
# perhaps you could ignore folders suffixed with `_` in the `test_build_examples` fn


def test_install_extension():
    FDIR_TESTDATA = FDIR_TESTS / "a4-portrait"
    FDIR_EXTENSION_INSTALL_PTH = FDIR_TESTDATA / "_extensions" / "document-issue-report"
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
        ["quarto", "render", "document.md", "--to", "document-issue-report-pdf"]
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
        ["quarto", "render", "document.md", "--to", "document-issue-report-pdf"]
    )
    assert FPTH_OUTPUT.exists()
    FPTH_LOG = FDIR_TESTDATA / "document.log"
    assert (
        not FPTH_LOG.exists()
    )  # log file should be deleted if Quarto PDF compilation is successful


def test_build_examples():
    EXAMPLE_DIRS = [
        i
        for i in (FDIR_ROOT / "examples").glob("*/")
        if "resource-path" not in i.name and "quarto-yaml" not in i.name
    ]  # TODO: Need to fix resource-path and quarto-yaml examples for this test
    for EXAMPLE_DIR in EXAMPLE_DIRS:
        FPTH_OUTPUT = EXAMPLE_DIR / "document.pdf"
        FPTH_OUTPUT.unlink(missing_ok=True)
        os.chdir(EXAMPLE_DIR)
        subprocess.run(["quarto", "add", str(FDIR_ROOT), "--no-prompt"])
        subprocess.run(
            ["quarto", "render", "document.md", "--to", "document-issue-report-pdf"]
        )
        assert FPTH_OUTPUT.exists()
        FPTH_LOG = EXAMPLE_DIR / "document.log"
        assert (
            not FPTH_LOG.exists()
        )  # log file should be deleted if Quarto PDF compilation is successful

@pytest.mark.skip(reason="@ollyhensby could you take a look... failing... maybe extensions were renamed?")
def test_build_quarto_yaml():
    FDIR = FDIR_ROOT / "examples" / "tables-docissue-in-quarto-yaml"
    FPTH_INPUT = FDIR / "document.md"
    FPTH_OUTPUT = FDIR / "document.pdf"
    FPTH_LOG = FDIR / "document.log"
    
    subprocess.run(["quarto", "add", str(FDIR_ROOT), "--no-prompt"])
    subprocess.run(["quarto", "render", str(FPTH_INPUT)])
    assert FPTH_OUTPUT.exists()
    assert not FPTH_LOG.exists()


def test_build_document_properties():
    FDIR = FDIR_ROOT / "examples" / "document-properties"
    FPTH_INPUT = FDIR / "document.md"
    FPTH_OUTPUT = FDIR / "document.pdf"
    FPTH_LOG = FDIR / "document.log"
    subprocess.run(["quarto", "add", str(FDIR_ROOT), "--no-prompt"])
    subprocess.run(
        ["quarto", "render", str(FPTH_INPUT), "--to", "document-issue-report-pdf"]
    )
    assert FPTH_OUTPUT.exists()
    assert not FPTH_LOG.exists()

    checked_props = check_quarto_doc_properties(FPTH_INPUT, FPTH_OUTPUT)
    assert all(item in ["title", "author", "subject"] for item in checked_props)
