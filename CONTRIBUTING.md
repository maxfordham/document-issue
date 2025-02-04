---
title: Development Installation
---

::: {.callout-warning}
`document-issue-xl` requires Windows to run. All other packages should work on both windows and linux but have only been tested on linux.
For dev instructions see: `packages/document-issue-xl/README.md`
:::

We use [pixi](https://prefix.dev/) to manage the monorepo.
If using VSCode, use the [`document-issue.code-workspace`](./.vscode/document-issue.code-workspace) file to open the project.
`pyproject.toml` files within each package allow then to be installed without the other packages.

To setup your dev environment run the following line-by-line in the repo ROOT:

```bash
curl -fsSL https://pixi.sh/install.sh | bash  # Install `pixi` (on linux) if req.
pixi install  # sets up env(s)
quarto install tinytex # TODO: move to env https://prefix.dev/channels/conda-forge/packages/r-tinytex
sudo apt-get update
sudo apt-get install libfontconfig  # `libfontconfig` if required
# ^^^ this should have setup your env

# we use [pixi tasks](https://pixi.sh/v0.22.0/features/advanced_tasks/) to manage dev actions
pixi run tests  # execute all tests in all pkgs
pixi task list  # list all tasks
pixi run test-document-issue # e.g. run tests for single pkg only
# pixi run doc-tests # TODO: add separate task that executes only tests req. for docs
pixi run preview-docs # preview quarto docs (note. this must be run after running tests)
```

::: {.callout-warning}
cntl+shift+p - python select interpreter set to default pixi env to be able to use vs code debugging features.
TODO: review if pixi vscode plugin can better handle this in future...
:::

## Github Actions

Docs are built and tests run on merge to `main` branch - see [workflows](https://github.com/maxfordham/document-issue/tree/main/.github/workflows) for details.

