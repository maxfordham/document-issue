---
title: "issuesheet"
---

::: {.callout-note collapse="true" icon=false}

## code

```py
# note. the tests are in the document-issue-io package
import pathlib
from document_issue_io.issuesheet import write_issuesheet_and_issuehistory


def delete_existing(fdir, glob_str):
    [x.unlink(missing_ok=True) for x in list(fdir.glob(glob_str))]


fdir_output, fdir_datapackage = pathlib.Path("tests/test-outputs"), pathlib.Path(
    "tests/datapackage"
)

glob_str = "03870-MXF*-IS-J-*.pdf"
delete_existing(fdir_output, glob_str)
fpth_issuesheet, fpths_issuehistory = write_issuesheet_and_issuehistory(
    fdir_datapackage
)


print(fpth_issuesheet.name, fpth_issuesheet.exists())
#> 03870-MXF-XX-XX-IS-J-00132.pdf True
print([f.name for f in fpths_issuehistory], [f.exists() for f in fpths_issuehistory])
#> ['03870-MXF-XX-XX-IS-J-00001.pdf', '03870-MXF-XX-XX-IS-J-00002.pdf'] [True, True]
```

:::

```{=html}
<embed src="test-outputs/03870-MXF-XX-XX-IS-J-00132.pdf" width="600px" height="500px" />
```

## Issue History

```{=html}
<embed src="test-outputs/03870-MXF-XX-XX-IS-J-00001.pdf" width="600px" height="500px" />
```

```{=html}
<embed src="test-outputs/03870-MXF-XX-XX-IS-J-00002.pdf" width="600px" height="500px" />
```
