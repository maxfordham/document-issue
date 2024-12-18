import json
import pathlib
import pandas as pd

with open(pathlib.Path(__file__).parent / "response_1734023393344.json") as f:
    data = json.load(f)

new_data = []
for di in data["data"]:
    new_di = {}
    for k, v in di.items():
        if k in ["InstanceReference", "TypeMark", "TypeSpecId", "Id"]:
            continue
        if v is True:
            v = "Yes"
        elif v is False:
            v = "No"
        if k == "Mark":
            new_di[k] = v
        else:
            if data["$schema"]["items"]["properties"][k]["unit"]:
                v = f"{v} _{data["$schema"]["items"]["properties"][k]["unit"]}_"
            new_di[data["$schema"]["items"]["properties"][k]["title"]] = v
    new_data.append(new_di)

df = pd.DataFrame(new_data)

columns = ["Mark"] + [
    v["title"]
    for _, v in data["$schema"]["items"]["properties"].items()
    if v["title"] in df.columns
]

df = df[columns]
df.columns = [f"__{c}__" for c in df.columns]
df.set_index("__Mark__", inplace=True)
df.fillna("", inplace=True)
with open(pathlib.Path(__file__).parent / "table.md", "w") as f:
    f.write(df.to_markdown(tablefmt="grid", stralign="left"))
