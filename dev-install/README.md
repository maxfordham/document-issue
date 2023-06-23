# Document Issue Development Install

```console
# run line by line

mamba env create -f environment-dev.yml
mamba activate document-issue-dev
# ^ base install of dev env (python, pytest, black etc.)

python getreqs.py
pip install requirements-dev.txt
# ^ looks in `pyproject.toml` files in each package and produces `requirements-dev.txt` file
#   pip install reqs

pip install -e ../packages/document-issue ../packages/document-issue-api ../packages/document-issue-io
# ^ install editable versions of each package
```