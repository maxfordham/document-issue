import os
import pathlib
import subprocess
from contextlib import contextmanager

@contextmanager
def change_dir(directory):
    current_dir = os.getcwd()
    os.chdir(directory)
    try:
        yield
    finally:
        os.chdir(current_dir)

def install_document_issue_quarto_extension(branch: str="main"):
    subprocess.run([
        "quarto", 
        "add", 
        f"maxfordham/document-issue/packages/document-issue-quarto@{branch}",
        "--no-prompt"
    ])

def update_document_issue_quarto_extension(branch: str="main"):
    subprocess.run([
        "quarto", 
        "update", 
        f"maxfordham/document-issue/packages/document-issue-quarto@{branch}",
        "--no-prompt"
    ])

def install_or_update_document_issue_quarto_extension(branch: str="main"):
    FPTH_EXT_INSTALL_PTH = pathlib.Path(__file__).parent / "_extensions" / "document-issue-schedule"
    if not FPTH_EXT_INSTALL_PTH.exists():
        install_document_issue_quarto_extension(branch=branch)
    else:
        update_document_issue_quarto_extension(branch=branch)