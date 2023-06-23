# document-issue-api

[![PyPI - Version](https://img.shields.io/pypi/v/document-issue-api.svg)](https://pypi.org/project/document-issue-api)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/document-issue-api.svg)](https://pypi.org/project/document-issue-api)

-----

**Table of Contents**

- [document-issue-api](#document-issue-api)
  - [Installation](#installation)
  - [Development Install](#development-install)
  - [License](#license)

## Installation

```console
pip install document-issue-api
```

## Development Install

├── packages
│   ├── document-issue
│   │   ├── pyproject.toml
│   │   ├── tests
│   │   ├── src
│   │   ├── ...
│   ├── document-issue-api
│   │   ├── pyproject.toml
│   │   ├── tests
│   │   ├── src
│   │   ├── ...

```console
mamba create -n document-issue-api-dev python pip pytest black jupyterlab
# create a new dev env

pip install -e .
pip install -e ../aecschedule
```

## License

`document-issue-api` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.