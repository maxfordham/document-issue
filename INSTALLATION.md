---
title: Development Installation
---

::: {.callout-warning}
`document-issue-xl` requires Windows to run. 
For dev instructions see: `packages/document-issue-xl/README.md`
:::

We use [pixi](https://prefix.dev/) to manage the monorepo. Install `pixi` (on linux) with the following command:

```bash
curl -fsSL https://pixi.sh/install.sh | bash
```

If using VSCode, we recommend using the [`document-issue.code-workspace`](./.vscode/document-issue.code-workspace) file to open the project.

To install the environment and packages for development, run the following commands from ROOT:

```bash
pixi install
```

cntl+shift+p - python select interpreter - set to pixi env. TODO: add pixi vscode plugin?

Install latex engine:

```bash
quarto install tinytex # TODO: should this be within the env?
```

Install `libfontconfig` if required:

```bash
sudo apt-get update
sudo apt-get install libfontconfig
```
