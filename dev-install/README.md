# Document Issue Development Install

```console
# run line by line

mamba env create -f environment-dev.yml
mamba activate document-issue-dev
# ^ base install of dev env (python, pytest, black etc.)

pip install -e ../packages/document-issue 
pip install -e ../packages/document-issue-api 
pip install -e ../packages/document-issue-io
# ^ install editable versions of each package
```
