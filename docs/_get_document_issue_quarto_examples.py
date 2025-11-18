import pathlib
import shutil

html = "{=html}"
callout = "{.callout-note collapse='true'}"
PAGE = """
---
title: "{name}"
---

::: {callout}
## Markdown Source File

````
{md}
````
:::

```{html}
<embed src="{name}/document.pdf" width="600px" height="1000px"/>
```
"""

fdir_src = pathlib.Path(__file__).parent.parent / "packages" / "document-issue-quarto" / "tests" / "test-outputs"
fdir_dst = pathlib.Path(__file__).parent / "document-issue-quarto-examples"
fdir_dst.mkdir(exist_ok=True)
fpths = fdir_src.glob("**/document.pdf")
for x in fpths:
    fpth_md = x.with_suffix(".md")
    md = fpth_md.read_text() if fpth_md.exists() else "(no markdown source file)"
    name = x.parent.stem
    text = PAGE.format(name=name, html=html, callout=callout, md=md) # , md=md
    file = (fdir_dst / f"{name}.qmd").write_text(text)
    fdir = fdir_dst / name
    fdir.mkdir(exist_ok=True)
    shutil.copyfile(x, (fdir / "document.pdf"))


print("retrieved examples from document-issue-quarto")
