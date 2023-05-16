# document-issue

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI - Version](https://img.shields.io/pypi/v/document-issue.svg)](https://pypi.org/project/document-issue)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/document-issue.svg)](https://pypi.org/project/document-issue)

-----

## Installation

```console
pip install document-issue  # TODO: when it is public
```

## Scope

`document-issue` defines the metadata required to accompany every issued document during the course of
a AEC (Architecture, Engineering, Construction) project.

Generally speaking each document must contain the following information to situate it within a project:

- a summary description
- when it was issued
- for what purpose
- by who

This package formalises those information fields and
defines a schema for storing them in a consistent manor. The structure is compliant
with BS EN ISO 19650-2. The information fields defined here may not required to be
shown in every document issued, but the aspiration is that no issued document
will require any additional datafields to those defined here. For internal use it
is suggested that all the information fields are competed to ensure a consistent
record of issued information is maintained.

```{Note}
for now, `document-issue` intentionally avoids considering the datafields that
are used to create the Document Number, this may follow up in the future.
```

## License

`document-issue` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

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
