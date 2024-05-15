import os
import pathlib
import subprocess
from contextlib import contextmanager

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
