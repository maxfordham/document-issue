---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.5
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

```{include} ../README.md
```

## Report Format Document

The pdf below is generated from the data defined above, but outputted as a
Max Fordham branded A4 report format document.

```{code-cell} ipython3
:tags: [remove-cell]

# from IPython.display import IFrame
# mh = MarkdownIssue(dh, tomd=True, todocx=True) # 
```

```{code-cell} ipython3
:tags: [remove-input]
# NOTE: 
# user action - save docx file as pdf
from ipyautoui.autodisplay_renderers import preview_pdf
preview_pdf("06667-MXF-XX-XX-SH-M-20003-header.pdf")
```

## User Interface

```{figure} images/ui.png
---
name: user interface
---
demonstrates how the document issue information is defined in the app
```
