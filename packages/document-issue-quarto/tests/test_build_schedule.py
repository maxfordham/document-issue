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
    FPTH_LOG = FDIR_TESTDATA / "document.log"
    assert (
        not FPTH_LOG.exists()
    )  # log file should be deleted if Quarto PDF compilation is successful


def test_build_examples():
    EXAMPLE_DIRS = [
        i
        for i in (FDIR_ROOT / "examples").glob("*/")
        if "resource-path" not in i.name or "quarto-yaml" not in i.name
    ]
    for EXAMPLE_DIR in EXAMPLE_DIRS:
        FPTH_OUTPUT = EXAMPLE_DIR / "document.pdf"
        FPTH_OUTPUT.unlink(missing_ok=True)
        os.chdir(EXAMPLE_DIR)
        subprocess.run(["quarto", "add", str(FDIR_ROOT), "--no-prompt"])
        subprocess.run(
            ["quarto", "render", "document.md", "--to", "document-issue-pdf"]
        )
        assert FPTH_OUTPUT.exists()
        FPTH_LOG = EXAMPLE_DIR / "document.log"
        assert (
            not FPTH_LOG.exists()
        )  # log file should be deleted if Quarto PDF compilation is successful


def test_build_quarto_yaml():
    FDIR = FDIR_ROOT / "examples" / "tables-docissue-in-quarto-yaml"
    FPTH_OUTPUT = FDIR / "document.pdf"
    FPTH_LOG = FDIR / "document.log"
    subprocess.run(["quarto", "add", str(FDIR_ROOT), "--no-prompt"])
    subprocess.run(["quarto", "render", "document.md"])
    assert FPTH_OUTPUT.exists()
    assert not FPTH_LOG.exists()
