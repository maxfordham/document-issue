# Document Issue IO

[![PyPI - Version](https://img.shields.io/pypi/v/document-issue-io.svg)](https://pypi.org/project/document-issue-io)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/document-issue-io.svg)](https://pypi.org/project/document-issue-io)

Document Issue IO is a Python package for generating PDF documents from
document issue information using Quarto and ReportLab.

-----

## Issue Sheet and Issue History Document Numbers

how is the `VWXYZ` number generated?
- e.g. 03870-MXF-XX-XX-IS-J-00001
- `VW` = `00` always 


### Issue History

- The issue history document numbers don't change throughout the course of the project. 
- The first issue history document has a `XYZ` = `001`, 
- when there are more issue columns than can fit on the page, another issue history document is produced, `XYZ` = `002`, and so on...

### Issue Sheet

- There is a unique Issue Sheet and document number for every issue (column in DNG spreadsheet). 
- The `XYZ` = 100 + [number of issues on project]
  - so the 14th issue Issue Sheet number will be `114`
  - this gives 899 potential issues which should be sufficient for our projects. 
- If you create an issue sheet with multiple issues, it will use the first issue you selected to create the number (*maybe this needs revising in the future*).


```py

def document_number(selected_issue_index, history, part):
    """number has the form VWXYZ"""
    VW = "00"  # by definition
    if history:
        if part < 1:
            XYZ = "001"
        elif part < 10:
            XYZ = "00" + str(int(part))
        else:
            XYZ = "0" + str(int(part))
    else:
        XYZ = str(int(selected_issue_index + 100))
    return VW + XYZ

```

## Installation

```bash
pip install document-issue-io
quarto install tinytex

# if required... 
sudo apt-get update
sudo apt-get install libfontconfig
```

**NOTE**: the `quarto` command installs the latex engine. This command should be put in the `postBuild` file in repo2docker repos. 
An alternative might be to add [r-tinytex](https://anaconda.org/conda-forge/r-tinytex) to the mamba file but I just tried that and it didn't work... 


## Building

To build the package, run the following command in the root of the package:

```bash
hatch build
```

This will first package the Document Issue Quarto extensions, [_extensions/](../document-issue-quarto/_extensions/),
as a tar file and move it to the templates directory. Then, it will build the package as normal and place it in
the `dist` directory.

The hatch build hook that packages the Quarto extensions is defined in the [hatch_build.py](hatch_build.py) file.

## License

`document-issue-io` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
