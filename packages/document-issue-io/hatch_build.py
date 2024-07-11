import os
import pathlib
import subprocess
import shutil
from contextlib import contextmanager

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

FDIR_DOCUMENT_ISSUE_QUARTO = pathlib.Path(__file__).parents[1] / "document-issue-quarto"
DIR_TEMPLATES = (
    pathlib.Path(__file__).parent / "src" / "document_issue_io" / "templates"
)


@contextmanager
def change_dir(directory):
    current_dir = os.getcwd()
    os.chdir(directory)
    try:
        yield
    finally:
        os.chdir(current_dir)


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        """Build the document-issue-quarto package and move the tarball to the
        document-issue-io package into the templates directory."""
        tar_name = "document-issue-quarto.tar.gz"
        with change_dir(FDIR_DOCUMENT_ISSUE_QUARTO):
            subprocess.run(
                [
                    "tar",
                    "cvzf",
                    tar_name,
                    "_extensions",
                ]
            )
            shutil.move(tar_name, DIR_TEMPLATES / tar_name)
