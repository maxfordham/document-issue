
Filename codes: 
----------------
tpl = templates
spec = specifications
opp = opportunities
tut = tutorials
wip = work-in-progress
dev = development / code section

To build, do the following: 

**note: we assume you are in the same dir as this README.txt file. 

create conda environment
```bash
mamba env create -f environment.yml
```

1. delete the ../src/__init.py
^ this is here for dev only

2. generate conf.py file from jupyterbook
>>> jupyter-book config sphinx .

3. generate docs
>>> sphinx-build . _build/html -b html

Notes.
- when authoring notebooks that will be executed the notebook must be authored from directly within the environment - __not__ using nb_conda_kernels