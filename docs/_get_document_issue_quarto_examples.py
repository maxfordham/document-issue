import pathlib
import shutil

PAGE = """
---
title: "{name}"
---

```{html}
<embed src="{name}/document.pdf" width="600px" height="1000px"/>
```
"""

fdir_src = pathlib.Path(__file__).parent.parent / "packages" / "document-issue-quarto" / "tests" / "test-outputs"
fdir_dst = pathlib.Path(__file__).parent / "document-issue-quarto-examples"
fdir_dst.mkdir(exist_ok=True)
fpths = fdir_src.glob("**/document.pdf")
for x in fpths:
    name = x.parents._tail[-2]
    text = PAGE.format(name=name, html="{=html}")
    file = (fdir_dst / f"{name}.qmd").write_text(text)
    fdir = fdir_dst / name
    fdir.mkdir(exist_ok=True)
    shutil.copyfile(x, (fdir / "document.pdf"))



print("retrieved examples from document-issue-quarto")
