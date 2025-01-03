---
title: "title-block-a4-p"
---

::: {.callout-note collapse="true" icon=false}

## title-block-a4-p

```py
import pathlib
from document_issue import demo_document_issue
from document_issue_io.title_block import title_block_a4

fdir = pathlib.Path("tests/test-outputs")
fpth = fdir / "title-block-a4-p.pdf"
fpth.unlink(missing_ok=True)
document_issue = demo_document_issue()
title_block_a4(document_issue=document_issue, fpth_output=fpth)

print(fpth.exists())
#> True
```

:::

```{=html}
<embed src="test-outputs/title-block-a4-p.pdf" width="600px" height="1000px" />
```
