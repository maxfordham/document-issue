"""
THIS FILE BUILDS THE DOCS LOCALLY USING JUPYTERBOOK AND SPHINX
# you must have a file called "GITHUB_TOKEN" in this 
# dir with nothing but your personal Github token inside
# this file is unique per user and will be ignored by Git
"""

import subprocess
import pathlib
import os
import sys

sys.path.append(str(pathlib.Path(__file__).parents[1] / "src"))

from document_issue.document import DocumentIssue

fdir = pathlib.Path(__file__).parents[1].resolve()
GITHUB_TOKEN = (fdir / "TOKENS" / "GITHUB_TOKEN").read_text()
CONF = pathlib.Path("conf.py")


script_erd = fdir / "_create_erd.py"
subprocess.call(f"python {str(script_erd)}", shell=True)
# ^ create ERD diagram

dh = DocumentIssue()
path_schema = pathlib.Path("schema.md")
dh.file_mdschema(path_schema)
_schema = path_schema.read_text().split("\n")
_schema[0] = "# Document Issue Schema\n"
path_schema.write_text("\n".join(_schema))

env = os.environ.copy()
env["SPHINX_GITHUB_CHANGELOG_TOKEN"] = GITHUB_TOKEN
# ^ add SPHINX_GITHUB_CHANGELOG_TOKEN to environ

subprocess.call("jupyter-book config sphinx .", shell=True)
# ^ create `conf.py` file

_conf = CONF.read_text().split("\n")
_conf = (
    _conf
    + ["import os"]
    + [
        'sphinx_github_changelog_token = os.environ.get("SPHINX_GITHUB_CHANGELOG_TOKEN")'
    ]
)
CONF.write_text("\n".join(_conf))
# ^ udpate `conf.py` file

subprocess.call("sphinx-build . _build/html -b html", shell=True, env=env)
# ^ call sphinx build with required environ vars

import shutil

src = "06667-MXF-XX-XX-SH-M-20003-header.pdf"
dst = "_build/html/06667-MXF-XX-XX-SH-M-20003-header.pdf"
shutil.copyfile(src, dst)
