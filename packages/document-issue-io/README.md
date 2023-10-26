# Document Issue IO

[![PyPI - Version](https://img.shields.io/pypi/v/document-issue-io.svg)](https://pypi.org/project/document-issue-io)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/document-issue-io.svg)](https://pypi.org/project/document-issue-io)

Document Issue IO is a Python package for generating PDF documents from
document issue information using Quarto and ReportLab.

-----

## Installation

```bash
pip install document-issue-io
```

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
