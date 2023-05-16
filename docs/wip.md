```{code-cell} ipython3
:tags: [remove-input]

import sys
import pathlib
fdir = (pathlib.Path(".").resolve().parent / "src")
sys.path.append(str(fdir))
from document_issue.document import DocumentIssue, MarkdownIssue
from document_issue.utils import preview_dict_as_yaml
dh = DocumentIssue()
preview_dict_as_yaml(dh.dict())
```



# Scope

```{code-cell} ipython3
:tags: [remove-cell]

import pathlib
from IPython.display import display, Markdown

li = pathlib.Path("../README.md").read_text().split("\n")
rng = [n for n,l in enumerate(li) if "## Scope" in l or "## License" in l]

display(Markdown(("\n").join(li[rng[0]:(rng[1]-1)])))
```