# document-issue

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Test](https://github.com/maxfordham/document-issue/actions/workflows/test-python-package.yml/badge.svg)](https://github.com/maxfordham/document-issue/actions/workflows/test-python-package.yml)

`document-issue` information defines the metadata required to accompany every issued document during the course of
an AEC (Architecture, Engineering, Construction) project.

Generally speaking each document must contain the following information to situate it within a project:

- a unique code, name, title and summary description
- categorisation information that defines to what the document pertains
- when it was issued, at what version
- by who
- for what purpose

The `document-issue` package formalises those information fields and
defines a schema for storing them consistently. The structure is compliant
with BS EN ISO 19650-2. The information fields defined here may not be required to be
output in every document issued, but the aspiration is that no issued document
will require any additional data-fields to those defined here. For internal use it
is suggested that all the information fields are competed to ensure a consistent
record of issued information is maintained.

As a suite of tools, the packages in the **document-issue** monorepo provide:

- a schema and datastore of the `document-issue` meta-data that accompanies every document
- a simple application interface for users to manage the issue history of documents on a project
- a Revit toolbar to support Revit sync
- standardised report format document templates for schedules and other report style documents

## Repo-structure

This project is structured as a monorepo. In the `packages` directory, each package is built and installable independently. Using the VS Code you can open the monorepo as a multi-package workspace defined in `.vscode/document-issue.code-workspace`.

## Packages

- `document-issue`: schema definitions (as pydantic models) defining document-issue information fields.
  - ***future*** *Includes logic for building document codes from categorisation fields.*
- `document-issue-io`: provides input/output functionality. Currently its main use is to define the markdown first couple of pages for report format documents.
- `document-issue-quarto`: defines the quarto/latex templates for creating branded report format documents. Used with `document-issue-io`.
- ***future*** *`document-issue-api`: API and associated database that maintains a reference of documents issued across projects.*
- ***future*** *`document-issue-ui`: user application for Engineers and Project Administrators for creating document codes and recording issued documents.*
- `document-issue-xl`: excel DNG and issue sheet generation
- ***future*** *`document-issue-pyrevit`: pyRevit toolbar to create sheets and views by interacting with the `document-issue-api`.*


```{Note}
for now, `document-issue` intentionally avoids considering the datafields that
are used to create the Document Number, this may follow up in the future.
```

## License

`document-issue` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.


## Development Install

```{warning}
`document-issue-xl` requires Windows to run. 
For dev instructions see: `packages/document-issue-xl/README.md`
```

If using VSCode, we recommend using the [`document-issue.code-workspace`](./.vscode/document-issue.code-workspace) file to open the project.

To install the environment and packages for development, run the following commands:

```console
# run line by line

mamba env create -f environment.yml
mamba activate document-issue-dev
mamba install xlwings #  left out of standard install due to Win dependency
# ^ base install of dev env (python, pytest, black etc.)

pip install -e packages/document-issue-ui
# ^ remove ui install from env file as the env file is used for CI 
#   and we don't need the ui deps for CI tests. 

quarto install tinytex
# ^ installs latex engine...

# if required... 
sudo apt-get update
sudo apt-get install libfontconfig
```

## Example `document-issue` data

```yaml
classification: Ac_05
doc_source: WD
document_description: Document Description
document_name: 06667-MXF-XX-XX-SH-M-20003
format_configuration:
  date_string_format: '%d %^b %y'
  description_in_filename: false
  include_author_and_checked_by: false
issue_history:
- author: EG
  checked_by: CK
  date: 2020-01-02
  issue_format: cde
  issue_notes: ''
  revision: P01
  status_code: S2
  status_description: Suitable for information
name_nomenclature: project code-originator-volume-level-type-role-number
notes:
- add notes here
originator: Max Fordham LLP
project_name: In House App Testing
project_number: J5001
roles:
- name: JG
  role: Project Engineer
scale: NTS
size: 
```
