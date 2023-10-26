import os
import pathlib
import subprocess
from contextlib import contextmanager

from document_issue_io.constants import FDIR_ARCHIVES

INSTALL_TAR = str(FDIR_ARCHIVES / "document-issue-quarto-v0.1.0.tar.gz")


@contextmanager
def change_dir(directory):
    current_dir = os.getcwd()
    os.chdir(directory)
    try:
        yield
    finally:
        os.chdir(current_dir)


def install_document_issue_quarto_extension():
    subprocess.run(["quarto", "add", INSTALL_TAR, "--no-prompt"])


def update_document_issue_quarto_extension():
    subprocess.run(["quarto", "update", INSTALL_TAR, "--no-prompt"])


def install_or_update_document_issue_quarto_extension():
    FPTH_EXT_INSTALL_PTH = pathlib.Path.cwd() / "_extensions" / "document-issue"
    if not FPTH_EXT_INSTALL_PTH.exists():
        install_document_issue_quarto_extension()
    else:
        update_document_issue_quarto_extension()
