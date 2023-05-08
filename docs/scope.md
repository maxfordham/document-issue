---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.0
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Scope

Every issued document must contain information to situate it within a project:

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

Refer to [Document Issue Schema](/docs/schema.md) for descriptions of the information
fields. Refer to [Current Templates](/current-templates) to see what is
currently being shown on contractual information.

```{Note}
that the schema below intentionally avoids considering the datafields that are used to create the Document Number.
```

## Example Document Issue Data

See below for an example of the data output defined by the Document Issue schema.

```{code-cell} ipython3
:tags: [remove-input]
import sys
import pathlib
fdir = (pathlib.Path(".").resolve().parent / "src")
sys.path.append(str(fdir))
from document_issue.document import DocumentHeader
from document_issue.utils import preview_dict_as_yaml
dh = DocumentHeader()
preview_dict_as_yaml(dh.dict())
```
