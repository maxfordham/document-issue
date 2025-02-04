import json
import pathlib

import pandas as pd
from document_issue.meta import LookupData


def dict_to_df(di):
    li = [{"code": k, "description": v} for k, v in di.items()]
    df = pd.DataFrame(li)
    return df



DIR = pathlib.Path(__file__).parent
lkup = LookupData.model_validate(json.loads((DIR / "lookup.json").read_text()))
li = ["classification", "doc_source", "level", "issue_format", "size", "status", "type"]

for x in li:
    df = dict_to_df(getattr(lkup, x))
    df.to_csv(DIR/ "data" /f"{x}.csv", index=None)

# package = describe("*.csv")
# package.to_json("datapackage.json")


print("done")
