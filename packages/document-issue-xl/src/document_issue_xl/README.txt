Create env:

```console
micromamba create -n compile python pydantic>2 numpy<2 cx_Freeze pandas Pillow PyYAML reportlab xlsxwriter xlwings frictionless -c conda-forge
micromamba activate compile
pip install -e ../../../document-issue -e ../../../document-issue-io 
#pip install git+https://git@github.com/maxfordham/document-issue.git@main#subdirectory=packages/document-issue git+https://git@github.com/maxfordham/document-issue.git@main#subdirectory=packages/document-issue-io
```

TO Compile:
	1. on command line: `python setup.py build` in this directory
	2. test by changing filepath in the macro in the excel vba of the Engineering Document Number Generator.xlsm
	3. rename build_vX_Y_Z to build to publish
	4. update table below.
	
version 0.2.1: python setup.py build

Version    | Date      |Commit	   |Current?   |Notes	
-----------+-----------+-----------+-----------+-----------
0.3.0		12/10/20	94b7a9e		*			New features and bugs fixed. Mainly custome filename format. See commits for bugs.
0.2.1		09/08/19	1ea2a34					Recovery of .exe after accidental overwrite
0.2.0		13/05/19	d312e4b					Complete restlying and updates to spreadsheet. Version in backup appears sparse.
0.1.6		10/05/19	391a5a6					Moved configs from Y: to J:
0.1.5		08/05/19	932586e					Spreadsheet updates
0.1.4		08/05/19	8e98903					Empty
0.1.3		30/04/19	---?---
0.1.2		26/04/19	---?---	
0.1.1		26/04/19	---?---					Short lived no changes.
0.1.0		29/03/19	---?---
0.0.3		20/03/19	---?---					First gen alpha version not safe.
	
