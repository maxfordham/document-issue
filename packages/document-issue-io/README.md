# Document Issue IO

[![PyPI - Version](https://img.shields.io/pypi/v/document-issue-io.svg)](https://pypi.org/project/document-issue-io)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/document-issue-io.svg)](https://pypi.org/project/document-issue-io)

Document Issue IO is a Python package for generating PDF documents from
document issue information using Quarto and ReportLab.

-----

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
