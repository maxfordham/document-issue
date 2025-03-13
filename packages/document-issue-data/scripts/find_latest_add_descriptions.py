import pathlib

import pandas as pd
from _load_dng_data import get_docs
from _load_found_files import FDIR_FIND_FILES, load_found_files

FDIR_PROCESSED_1 = pathlib.Path(__file__).parent / "data-processed-1"
MAP_COLS_DOCS = {
    "project_number": "project",
    "document_code": "document-code",
    "uniclass": "uniclass",
    "Document Title": "title",
    # "User Defined Drawing Title",
    "Project Name": "project-name",
    # "Originator Description",
    "Information Type Description": "type",
    "Resulting Drawing Type Description": "drawing-type",
    "Volume Name": "volume",
    "System Identifier Description": "system",
    "Level Description": "level",
    # "X Sequence Number",
    # "YZ Sequence Number",
    # "Resulting Sequence Description",
    # "Additional User Defined Text",
    "Size": "size",
    "Scale": "scale",
    "Information Author": "author",
    "docSource": "src",
    # "Project",
    # "Originator",
    # "Volume",
    # "Level",
    # "Document Type",
    "Role": "role",
    "System Identifier": "sys-id",
    # "X",
    # "YZ",
    # "Number",
}
COLS_DOCS = list(MAP_COLS_DOCS.keys())


def to_list_of_dicts(data: dict[tuple[str, str], str]) -> list[dict[str, str]]:
    return [{"document_code": k[0], "date": k[1], "file_path": v} for k, v in data.items()]


def to_dateframe(data: dict[tuple[str, str], str]) -> pd.DataFrame:
    return pd.DataFrame(to_list_of_dicts(data)).sort_values(by="date")


def get_latest(data):
    df = to_dateframe(data)
    df["date"] = pd.to_datetime(df["date"])
    df["link"] = df["file_path"].apply(lambda x: pathlib.PurePath(r"J:/") / pathlib.PurePath(*pathlib.Path(x).parts[4:]))
    df["link"] = df.link.astype(str).str.replace("/", "\\")


    return df.sort_values(by="date", ascending=False).groupby("document_code").tail(1)

def tidy_drwg_subtype_ser(ser: pd.Series) -> pd.Series:
    ser = ser.fillna("-")
    ser.update(ser.map({' - Layout': "Layout"}).dropna())
    ser.update(ser.map({"6.0": "-"}))
    ser.update(ser.map({"0.0": "-"}))
    ser.update(ser.map({' - Detail': "Detail"}))
    ser.update(ser.map({' - Section': "Section"}))
    # ser.update(ser.map(' - House', "Detail"))
    ser.update(ser.map({' - Schematic': "Schematic"}))
    ser.update(ser.map({' - Site Layout': "Site Layout"}))
    ser.update(ser.map({' - Detail': "Detail"}))
    ser.update(ser.map({' - Strategy': "Strategy"}))
    ser.update(ser.map({'Only Applies to Drawings': "-"}))
    ser.update(ser.map({'Only Applies to Drawings and Sketches': "-"}))
    ser.update(ser.map({' - House': "House"}))

    unique = ser.unique()
    return ser


def merge_and_format(df_docs, df_paths):
    df = df_paths.merge(df_docs, on="document_code", how="left")
    df = df[["link", "date", *COLS_DOCS]]
    df = df.rename(columns=MAP_COLS_DOCS)
    df["drawing-type"] = tidy_drwg_subtype_ser(df["drawing-type"])

    # find mis-categories schematics
    _1 = df.query("`drawing-type` != 'Schematic'")
    _1.title = _1.title.str.lower()
    _2 = _1[_1.title.fillna("").str.contains("schematic")]
    _2.loc[:, "drawing-type"] = "Schematic"
    df.update(_2)
    return df




if __name__ == "__main__":
    df_docs = get_docs()[COLS_DOCS]

    found, missing = load_found_files(list(FDIR_FIND_FILES.glob("found_files*.txt")))

    # latest
    df_latest = get_latest(found | missing).merge(df_docs, on="document_code", how="left")
    df_latest.to_csv(FDIR_PROCESSED_1 / "latest.csv", index=False)

    # latest found
    df_paths = get_latest(found)
    df_latest_found = merge_and_format(df_docs, df_paths)
    


    df_latest_found.to_csv(FDIR_PROCESSED_1 / "latest_found.csv", index=False)
    df_latest_found.to_csv(pathlib.Path(__file__).parent.parent / "dashboard" / "src" / "data" / "latest_found.csv", index=False)
    df_latest_found.loc[0:10].to_csv(pathlib.Path(__file__).parent.parent / "dashboard" / "src" / "data" / "tmp" / "latest_found.csv", index=False)

    # schematics
    df_latest_found_schematics = df_latest_found.query("`drawing-type` == 'Schematic'")
    df_latest_found_schematics.to_csv(FDIR_PROCESSED_1 / "latest_found_schematics.csv", index=False)
    df_latest_found_schematics.to_csv(pathlib.Path(__file__).parent.parent / "dashboard" / "src" / "data" / "latest_found_schematics.csv", index=False)


    # details
    df_latest_found_details = df_latest_found.query("`drawing-type` == 'Detail'")
    df_latest_found_details.to_csv(FDIR_PROCESSED_1 / "latest_found_details.csv", index=False)
    df_latest_found_details.to_csv(pathlib.Path(__file__).parent.parent / "dashboard" / "src" / "data" / "latest_found_details.csv", index=False)
    print("done")
