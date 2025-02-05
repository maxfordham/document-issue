import os
import shutil
import subprocess

from tests.constants import (
    FDIR_EXAMPLES_DOC_ISSUE_REPORT,
    FDIR_ROOT,
    FDIR_TEST_OUTPUT_DOC_ISSUE_REPORT,
)

# TODO:
# move examples to examples dir in root and setup to work with the documentation workflow.
# perhaps you could ignore folders suffixed with `_` in the `test_build_examples` fn


def test_install_extension():
    FDIR_EXAMPLE_DATA = FDIR_EXAMPLES_DOC_ISSUE_REPORT / "a4-portrait-report"
    FDIR_TESTDATA = FDIR_TEST_OUTPUT_DOC_ISSUE_REPORT / "a4-portrait-report"
    FDIR_TESTDATA.mkdir(exist_ok=True)
    shutil.copytree(FDIR_EXAMPLE_DATA, FDIR_TESTDATA, dirs_exist_ok=True)
    FDIR_EXTENSION_INSTALL_PTH = FDIR_TESTDATA / "_extensions" / "document-issue-report"
    if FDIR_EXTENSION_INSTALL_PTH.exists():
        shutil.rmtree(FDIR_EXTENSION_INSTALL_PTH)
    os.chdir(FDIR_TESTDATA)
    subprocess.run(["quarto", "add", str(FDIR_ROOT), "--no-prompt"], check=False)
    assert FDIR_EXTENSION_INSTALL_PTH.exists()


def test_build_schedule_a4_portrait():
    FDIR_EXAMPLE_DATA = FDIR_EXAMPLES_DOC_ISSUE_REPORT / "a4-portrait-report"
    FDIR_TESTDATA = FDIR_TEST_OUTPUT_DOC_ISSUE_REPORT / "a4-portrait-report"
    FDIR_TESTDATA.mkdir(exist_ok=True)
    shutil.copytree(FDIR_EXAMPLE_DATA, FDIR_TESTDATA, dirs_exist_ok=True)
    FPTH_OUTPUT = FDIR_TESTDATA / "document.pdf"
    FPTH_OUTPUT.unlink(missing_ok=True)
    os.chdir(FDIR_TESTDATA)
    subprocess.run(["quarto", "add", str(FDIR_ROOT), "--no-prompt"], check=False)
    subprocess.run(
        ["quarto", "render", "document.md", "--to", "document-issue-report-pdf"],
        check=False,
    )
    assert FPTH_OUTPUT.exists()
    FPTH_LOG = FDIR_TESTDATA / "document.log"
    assert not FPTH_LOG.exists()  # log file should be deleted if Quarto PDF compilation is successful


def test_build_schedule_a4_portrait_draft():
    FDIR_EXAMPLE_DATA = FDIR_EXAMPLES_DOC_ISSUE_REPORT / "a4-portrait-draft-report"
    FDIR_TESTDATA = FDIR_TEST_OUTPUT_DOC_ISSUE_REPORT / "a4-portrait-draft-report"
    FDIR_TESTDATA.mkdir(exist_ok=True)
    shutil.copytree(FDIR_EXAMPLE_DATA, FDIR_TESTDATA, dirs_exist_ok=True)
    FPTH_OUTPUT = FDIR_TESTDATA / "document.pdf"
    FPTH_OUTPUT.unlink(missing_ok=True)
    os.chdir(FDIR_TESTDATA)
    subprocess.run(["quarto", "add", str(FDIR_ROOT), "--no-prompt"], check=False)
    subprocess.run(
        ["quarto", "render", "document.md", "--to", "document-issue-report-pdf"],
        check=False,
    )
    assert FPTH_OUTPUT.exists()
    FPTH_LOG = FDIR_TESTDATA / "document.log"
    assert not FPTH_LOG.exists()  # log file should be deleted if Quarto PDF compilation is successful


def test_build_schedule_a3_landscape():
    FDIR_EXAMPLE_DATA = FDIR_EXAMPLES_DOC_ISSUE_REPORT / "a3-landscape-report"
    FDIR_TESTDATA = FDIR_TEST_OUTPUT_DOC_ISSUE_REPORT / "a3-landscape-report"
    FDIR_TESTDATA.mkdir(exist_ok=True)
    shutil.copytree(FDIR_EXAMPLE_DATA, FDIR_TESTDATA, dirs_exist_ok=True)
    FPTH_OUTPUT = FDIR_TESTDATA / "document.pdf"
    FPTH_OUTPUT.unlink(missing_ok=True)
    os.chdir(FDIR_TESTDATA)
    subprocess.run(["quarto", "add", str(FDIR_ROOT), "--no-prompt"], check=False)
    subprocess.run(
        ["quarto", "render", "document.md", "--to", "document-issue-report-pdf"],
        check=False,
    )
    assert FPTH_OUTPUT.exists()
    FPTH_LOG = FDIR_TESTDATA / "document.log"
    assert not FPTH_LOG.exists()  # log file should be deleted if Quarto PDF compilation is successful


def test_build_schedule_disclaimer_page():
    FDIR_EXAMPLE_DATA = FDIR_EXAMPLES_DOC_ISSUE_REPORT / "disclaimer-page"
    FDIR_TESTDATA = FDIR_TEST_OUTPUT_DOC_ISSUE_REPORT / "disclaimer-page"
    FDIR_TESTDATA.mkdir(exist_ok=True)
    shutil.copytree(FDIR_EXAMPLE_DATA, FDIR_TESTDATA, dirs_exist_ok=True)
    FPTH_OUTPUT = FDIR_TESTDATA / "document.pdf"
    FPTH_OUTPUT.unlink(missing_ok=True)
    os.chdir(FDIR_TESTDATA)
    subprocess.run(["quarto", "add", str(FDIR_ROOT), "--no-prompt"], check=False)
    subprocess.run(
        ["quarto", "render", "document.md", "--to", "document-issue-report-pdf"],
        check=False,
    )
    assert FPTH_OUTPUT.exists()
    FPTH_LOG = FDIR_TESTDATA / "document.log"
    assert not FPTH_LOG.exists()  # log file should be deleted if Quarto PDF compilation is successful


def test_build_schedule_document_properties():
    FDIR_EXAMPLE_DATA = FDIR_EXAMPLES_DOC_ISSUE_REPORT / "document-properties"
    FDIR_TESTDATA = FDIR_TEST_OUTPUT_DOC_ISSUE_REPORT / "document-properties"
    FDIR_TESTDATA.mkdir(exist_ok=True)
    shutil.copytree(FDIR_EXAMPLE_DATA, FDIR_TESTDATA, dirs_exist_ok=True)
    FPTH_OUTPUT = FDIR_TESTDATA / "document.pdf"
    FPTH_OUTPUT.unlink(missing_ok=True)
    os.chdir(FDIR_TESTDATA)
    subprocess.run(["quarto", "add", str(FDIR_ROOT), "--no-prompt"], check=False)
    subprocess.run(
        ["quarto", "render", "document.md", "--to", "document-issue-report-pdf"],
        check=False,
    )
    assert FPTH_OUTPUT.exists()
    FPTH_LOG = FDIR_TESTDATA / "document.log"
    assert not FPTH_LOG.exists()  # log file should be deleted if Quarto PDF compilation is successful


def test_build_schedule_footer():
    FDIR_EXAMPLE_DATA = FDIR_EXAMPLES_DOC_ISSUE_REPORT / "footer"
    FDIR_TESTDATA = FDIR_TEST_OUTPUT_DOC_ISSUE_REPORT / "footer"
    FDIR_TESTDATA.mkdir(exist_ok=True)
    shutil.copytree(FDIR_EXAMPLE_DATA, FDIR_TESTDATA, dirs_exist_ok=True)
    FPTH_OUTPUT = FDIR_TESTDATA / "document.pdf"
    FPTH_OUTPUT.unlink(missing_ok=True)
    os.chdir(FDIR_TESTDATA)
    subprocess.run(["quarto", "add", str(FDIR_ROOT), "--no-prompt"], check=False)
    subprocess.run(
        ["quarto", "render", "document.md", "--to", "document-issue-report-pdf"],
        check=False,
    )
    assert FPTH_OUTPUT.exists()
    FPTH_LOG = FDIR_TESTDATA / "document.log"
    assert not FPTH_LOG.exists()  # log file should be deleted if Quarto PDF compilation is successful


def test_build_schedule_images():
    FDIR_EXAMPLE_DATA = FDIR_EXAMPLES_DOC_ISSUE_REPORT / "images"
    FDIR_TESTDATA = FDIR_TEST_OUTPUT_DOC_ISSUE_REPORT / "images"
    FDIR_TESTDATA.mkdir(exist_ok=True)
    shutil.copytree(FDIR_EXAMPLE_DATA, FDIR_TESTDATA, dirs_exist_ok=True)
    FPTH_OUTPUT = FDIR_TESTDATA / "document.pdf"
    FPTH_OUTPUT.unlink(missing_ok=True)
    os.chdir(FDIR_TESTDATA)
    subprocess.run(["quarto", "add", str(FDIR_ROOT), "--no-prompt"], check=False)
    subprocess.run(
        ["quarto", "render", "document.md", "--to", "document-issue-report-pdf"],
        check=False,
    )
    assert FPTH_OUTPUT.exists()
    FPTH_LOG = FDIR_TESTDATA / "document.log"
    assert not FPTH_LOG.exists()  # log file should be deleted if Quarto PDF compilation is successful


def test_build_schedule_product_output():
    FDIR_EXAMPLE_DATA = FDIR_EXAMPLES_DOC_ISSUE_REPORT / "product-output"
    FDIR_TESTDATA = FDIR_TEST_OUTPUT_DOC_ISSUE_REPORT / "product-output"
    FDIR_TESTDATA.mkdir(exist_ok=True)
    shutil.copytree(FDIR_EXAMPLE_DATA, FDIR_TESTDATA, dirs_exist_ok=True)
    FPTH_OUTPUT = FDIR_TESTDATA / "document.pdf"
    FPTH_OUTPUT.unlink(missing_ok=True)
    os.chdir(FDIR_TESTDATA)
    subprocess.run(["quarto", "add", str(FDIR_ROOT), "--no-prompt"], check=False)
    subprocess.run(
        ["quarto", "render", "document.md", "--to", "document-issue-report-pdf"],
        check=False,
    )
    assert FPTH_OUTPUT.exists()
    FPTH_LOG = FDIR_TESTDATA / "document.log"
    assert not FPTH_LOG.exists()  # log file should be deleted if Quarto PDF compilation is successful


def test_build_schedule_resource_path():
    FDIR_EXAMPLE_DATA = FDIR_EXAMPLES_DOC_ISSUE_REPORT / "resource-path"
    FDIR_TESTDATA = FDIR_TEST_OUTPUT_DOC_ISSUE_REPORT / "resource-path"
    FDIR_TESTDATA.mkdir(exist_ok=True)
    shutil.copytree(FDIR_EXAMPLE_DATA, FDIR_TESTDATA, dirs_exist_ok=True)
    FPTH_OUTPUT = FDIR_TESTDATA / "document.pdf"
    FPTH_OUTPUT.unlink(missing_ok=True)
    os.chdir(FDIR_TESTDATA)
    subprocess.run(["quarto", "add", str(FDIR_ROOT), "--no-prompt"], check=False)
    subprocess.run(
        ["quarto", "render", "document.md", "--to", "document-issue-report-pdf", "--resource-path=./media"],
        check=False,
    )
    assert FPTH_OUTPUT.exists()
    FPTH_LOG = FDIR_TESTDATA / "document.log"
    assert not FPTH_LOG.exists()  # log file should be deleted if Quarto PDF compilation is successful


def test_build_schedule_table_of_contents():
    FDIR_EXAMPLE_DATA = FDIR_EXAMPLES_DOC_ISSUE_REPORT / "table-of-contents"
    FDIR_TESTDATA = FDIR_TEST_OUTPUT_DOC_ISSUE_REPORT / "table-of-contents"
    FDIR_TESTDATA.mkdir(exist_ok=True)
    shutil.copytree(FDIR_EXAMPLE_DATA, FDIR_TESTDATA, dirs_exist_ok=True)
    FPTH_OUTPUT = FDIR_TESTDATA / "document.pdf"
    FPTH_OUTPUT.unlink(missing_ok=True)
    os.chdir(FDIR_TESTDATA)
    subprocess.run(["quarto", "add", str(FDIR_ROOT), "--no-prompt"], check=False)
    subprocess.run(
        ["quarto", "render", "document.md", "--to", "document-issue-report-pdf"],
        check=False,
    )
    assert FPTH_OUTPUT.exists()
    FPTH_LOG = FDIR_TESTDATA / "document.log"
    assert not FPTH_LOG.exists()  # log file should be deleted if Quarto PDF compilation is successful


def test_build_schedule_tables():
    FDIR_EXAMPLE_DATA = FDIR_EXAMPLES_DOC_ISSUE_REPORT / "tables"
    FDIR_TESTDATA = FDIR_TEST_OUTPUT_DOC_ISSUE_REPORT / "tables"
    FDIR_TESTDATA.mkdir(exist_ok=True)
    shutil.copytree(FDIR_EXAMPLE_DATA, FDIR_TESTDATA, dirs_exist_ok=True)
    FPTH_OUTPUT = FDIR_TESTDATA / "document.pdf"
    FPTH_OUTPUT.unlink(missing_ok=True)
    os.chdir(FDIR_TESTDATA)
    subprocess.run(["quarto", "add", str(FDIR_ROOT), "--no-prompt"], check=False)
    subprocess.run(
        ["quarto", "render", "document.md", "--to", "document-issue-report-pdf"],
        check=False,
    )
    assert FPTH_OUTPUT.exists()
    FPTH_LOG = FDIR_TESTDATA / "document.log"
    assert not FPTH_LOG.exists()  # log file should be deleted if Quarto PDF compilation is successful


def test_build_docissue_in_quarto_yaml():
    FDIR_EXAMPLE_DATA = FDIR_EXAMPLES_DOC_ISSUE_REPORT / "docissue-in-quarto-yaml"
    FDIR_TESTDATA = FDIR_TEST_OUTPUT_DOC_ISSUE_REPORT / "docissue-in-quarto-yaml"
    FDIR_TESTDATA.mkdir(exist_ok=True)
    shutil.copytree(FDIR_EXAMPLE_DATA, FDIR_TESTDATA, dirs_exist_ok=True)
    FPTH_OUTPUT = FDIR_TESTDATA / "document.pdf"
    FPTH_OUTPUT.unlink(missing_ok=True)
    os.chdir(FDIR_TESTDATA)
    subprocess.run(["quarto", "add", str(FDIR_ROOT), "--no-prompt"], check=False)
    subprocess.run(
        ["quarto", "render", "document.md"],
        check=False,
    )
    assert FPTH_OUTPUT.exists()
    FPTH_LOG = FDIR_TESTDATA / "document.log"
    assert not FPTH_LOG.exists()  # log file should be deleted if Quarto PDF compilation is successful
