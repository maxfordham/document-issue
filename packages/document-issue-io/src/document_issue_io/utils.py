import os
import pathlib
import subprocess
import shutil
from contextlib import contextmanager

from document_issue.document_issue import DocumentIssue
from document_issue_io.title_block import build_schedule_title_page_template_pdf
from document_issue_io.constants import FDIR_TEMPLATES, FDIR_MEDIA

FPTH_INSTALL_TAR = FDIR_TEMPLATES / "document-issue-quarto.tar.gz"
FPTH_FOOTER_LOGO = FDIR_MEDIA / "footer-logo.png"


@contextmanager
def change_dir(directory):
    current_dir = os.getcwd()
    os.chdir(directory)
    try:
        yield
    finally:
        os.chdir(current_dir)


def install_document_issue_quarto_extension():
    subprocess.run(["quarto", "add", str(FPTH_INSTALL_TAR), "--no-prompt"])


def update_document_issue_quarto_extension():
    subprocess.run(["quarto", "update", str(FPTH_INSTALL_TAR), "--no-prompt"])


def install_or_update_document_issue_quarto_extension():
    FPTH_EXT_INSTALL_PTH = pathlib.Path.cwd() / "_extensions" / "document-issue"
    if not FPTH_EXT_INSTALL_PTH.exists():
        install_document_issue_quarto_extension()
    else:
        update_document_issue_quarto_extension()


def document_issue_md_to_pdf(
    document_issue: DocumentIssue, fpth_md: pathlib.Path, fpth_pdf: pathlib.Path
):
    """Convert markdown document issue to pdf using quarto."""
    with change_dir(fpth_md.parent):
        shutil.copy(
            FPTH_FOOTER_LOGO, FPTH_FOOTER_LOGO.name
        )  # Copy footer logo to markdown document issue directory
        build_schedule_title_page_template_pdf(document_issue=document_issue)
        install_or_update_document_issue_quarto_extension()
        subprocess.run(
            [
                "quarto",
                "render",
                fpth_md.name,
                "--to",
                "document-issue-pdf",
                "-o",
                fpth_pdf.name,
            ]
        )
        # NOTE: quarto render does not allow to specify a relative or absolute
        # path for "-o" parameter. Therefore, will just move post-render
        if fpth_pdf != fpth_md.parent / fpth_pdf.name:
            shutil.move(fpth_pdf.name, fpth_pdf)
