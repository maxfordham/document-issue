# mapping tables
import json
import os
import re
from typing import Any

import pandas as pd
import stringcase
import xlwings as xw
from constants import CONFIG_DIR, DEFAULT_CONFIG
from d_i_ui import warning_messagebox
from document_issue.meta import (
    DocumentCodeParts,
    DocumentMetadataMap,
    LookupData,
)


def index_of_value(value, sheet):
    """Look for a value in the spreadsheet"""
    for i, line in enumerate(xw.sheets[sheet].range((1, 1), (200, 200)).value):
        try:
            return (i + 1, line.index(value) + 1)
        except:
            pass
    return False


def get_table_data(name: str) -> dict:
    data = xw.sheets[name].range(index_of_value(f"{name}_code", name)).options(pd.DataFrame, expand="table").value
    des = f"{name}_des"
    # backwards compatibility

    if des not in data.columns:
        if "Comment" in data.columns:
            data[des] = data["Comment"]

    if name == "issueFormat" and des not in data.columns:
        data[des] = data["Status Description"]

    if name == "status" and des not in data.columns:
        di = dict(zip(data.index.to_list(), [l[0] for l in data["Revision"].to_list()]))
        data["rev_code"] = data.index.map(di)
        data[des] = (
            data["rev_code"]
            .str.cat(data["Status Description"], sep=" - ")
            .str.cat(data["Description"], sep=" - ")
            .str.cat(data["Revision"], sep=" - ")
        )

    return data[f"{name}_des"].to_dict()


def get_lookup_data() -> LookupData:  # get_lookup_data
    names = [k for k in list(DocumentCodeParts.__members__.keys()) if k != "sequence"]
    names = names + [
        stringcase.camelcase(f) for f in DocumentMetadataMap.model_fields.keys() if f not in ["classification_uniclass"]
    ]
    sheet_names = [s.name for s in xw.sheets]
    names = [n for n in names if n in sheet_names]
    data = {stringcase.snakecase(n): get_table_data(n) for n in names}

    # backwards compatibility
    if "type" not in sheet_names:
        data["type"] = get_table_data("infoType")

    # classification_uniclass
    name = "classification"
    df = xw.sheets[name].range(index_of_value(f"{name}_code", name)).options(pd.DataFrame, expand="table").value
    data["classification_uniclass"] = df["uniclass_classification"].to_dict()

    # sequence
    name = "sequence"
    type_sequences = (
        xw.sheets[name].range(index_of_value(f"{name}_code", name)).options(pd.DataFrame, expand="table").value
    )
    type_sequences = type_sequences.to_dict()
    type_sequences = {k: {_k: _v for _k, _v in v.items() if _v is not None} for k, v in type_sequences.items()}
    data["type_sequences"] = type_sequences

    # BUGFIX: ignore null classification fields
    data["classification"] = {k: v for k, v in data["classification"].items() if v is not None}

    return LookupData(**data | type_sequences)


def project_info():
    """Gets the project info from the first sheet"""
    return (
        xw.sheets["readme"]
        .range(index_of_value("Job Number", "readme"))
        .options(dict, expand="table", numbers=int)
        .value
    )


def get_issues(data):
    """Work out which columns are dates"""
    match_str = r"^20(\d{2}\d{2}\d{2})-.*$"  # string match date format 20YYMMDD-...
    # ^ Test here: https://regex101.com/r/qH0sU7/1
    return [c for c in data.columns if re.match(match_str, c) is not None]


def verify_config(config):
    for k in DEFAULT_CONFIG.keys():
        if k not in config:
            config[k] = DEFAULT_CONFIG[k]
    return config


def config_filename(job_number):
    """Return the filename of the config files."""
    # username = os.environ['username']
    return CONFIG_DIR + "\\" + str(job_number) + ".json"


def user_config(job_number):
    """Loads the user configuration"""
    file = config_filename(job_number)
    try:
        if os.path.isfile(file):
            with open(file) as handle:
                # config = pickle.load(handle)
                config = json.load(handle)
        else:
            config = DEFAULT_CONFIG
    except:
        warning_messagebox(
            "Cannot read Job Settings. We'll carry on anyway but contact support.",
            "Config error",
        )

    config = verify_config(config)
    return config


def get_pandas_data():
    """Extract data from spreadsheet and convert it to a pandas dataframe"""
    if index_of_value("Document Number", "1. Document Numbering"):
        res = (
            xw.sheets["1. Document Numbering"]
            .range(index_of_value("Sort By Uniclass", "1. Document Numbering"))
            .options(pd.Series, expand="table")
            .value
        )
        res = res.reset_index(drop=False).set_index("Document Number").rename(columns={"Sort By Uniclass": "uniclass"})
        if "Document Number" not in res.columns:  # backwards compatability for spreadsheet upgrade.
            res.index.names = ["Document Number Index"]
            res["Document Number"] = res.index

        if type(res) is pd.core.frame.Series:
            raise ValueError(
                "At least two documents required.\nOnly need one? Just add a dummy one",
            )
        if "Document Number" not in res.columns:
            res["Document Number"] = res.index
        res = res[res["Document Number"] != -2146826246]
        cols_to_remove = list(set(res.columns).intersection(map(str, range(999))))
        cols_to_remove += [
            x for x in res.columns if "Column" in x or "blank" in x or "→" in x or "?" in x or "Add to " in x
        ]
        res = res.sort_values("Document Number")
        res = res.dropna(subset=["Document Number"])
        pd.options.display.float_format = "{:,.0f}".format
        return res.drop(cols_to_remove, axis=1)  # remove column that are empty.
    raise Exception(
        "Cannot Revision Information - Something has gone wrong contact support.",
    )


def get_distribution_data(li_issues=None):
    if index_of_value("Name", "1. Document Numbering"):
        res = (
            xw.sheets["1. Document Numbering"]
            .range(index_of_value("Name", "1. Document Numbering"))
            .options(pd.Series, expand="table")
            .value
        )
        if type(res) is pd.core.frame.Series:
            raise ValueError(
                "Atleast two people in distribution required.\nOnly need one? Just add a dummy one",
            )
        res["Name"] = res.index  # TODO: this is bad
        res = res.fillna("")
        pd.options.display.float_format = "{:,.0f}".format

        if li_issues is not None:  # TODO: tbc
            cols = list(res.columns)
            for i, col in enumerate(li_issues):
                cols[i] = col
            res.columns = cols
            df = res[li_issues + ["Name"]]
            res = df.loc[df.index.notnull()]

        return res
    raise Exception(
        'Cannot Find Distribution Table - ensure First Column is titled "Name"',
    )


def read_excel(dump_package=True) -> Any:
    lookup = get_lookup_data()
    map_status_rev = {k: v.split(" - ")[0] for k, v in lookup.status.items()}
    projectinfo = project_info()
    config = user_config(projectinfo.get("Job Number"))  # define this in the UI
    data = get_pandas_data()
    li_issues = get_issues(data)
    doc_descriptions = data[[c for c in data.columns if c not in li_issues + ["Current Rev"]]].T.to_dict()
    doc_issues = data[li_issues].T.to_dict()

    def getlastrev(di, map_status_rev=map_status_rev):
        if set(di.values()) == {None}:
            return None
        li = []
        di = {k: v for k, v in di.items() if v is not None}
        for k, v in di.items():
            rev = map_status_rev[k.split("-")[1]]
            li.append(f"{k}-{rev}{v}")
        return li[-1]

    cols = data.columns.to_list()
    df_document = data[cols[0 : cols.index("Current Rev")]]

    doc_currentrevs = {}  # {k: getlastrev(v) for k, v in doc_issues.items()}
    for k, v in doc_issues.items():
        lastrev = getlastrev(v)
        if lastrev is not None:
            doc_currentrevs[k] = lastrev

    doc_distribution = get_distribution_data(li_issues=li_issues)
    df_distribution = doc_distribution.melt(
        id_vars=["Name"],
        var_name="date_status",
        value_name="issue_format",
    ).rename(columns={"Name": "recipient"})

    df_issue = data[li_issues]
    df_issue = (
        df_issue.reset_index()
        .rename(columns={"Document Number Index": "document_code"})
        .melt(
            id_vars=["document_code"],
            var_name="date_status",
            value_name="revision_number",
        )
        .dropna(subset=["revision_number"])
    )

    if dump_package:
        project_no = projectinfo["Job Number"]
        if project_no is None:
            raise ValueError("Project Number not found")
        if isinstance(project_no, int):
            project_no = f"J{project_no}"
        fdir_package = pathlib.Path(CONFIG_DIR) / project_no
        fdir_package.mkdir(exist_ok=True)
        dng_to_package(
            lookup,
            config,
            projectinfo,
            df_distribution,
            df_issue,
            df_document.reset_index().rename(
                columns={"Document Number Index": "document_code"},
            ),
            fdir=fdir_package,
        )

    return (
        lookup,
        projectinfo,
        config,
        data,
        li_issues,
        doc_currentrevs,
        doc_descriptions,
        doc_issues,
        doc_distribution,
    )


import pathlib
from contextlib import contextmanager
from pathlib import Path

from frictionless import Package, Resource
from frictionless.resources import JsonResource


@contextmanager
def set_directory(path: Path):
    """Sets the cwd within the context

    Args:
        path (Path): The path to the cwd

    Yields:
        None

    """
    origin = Path().absolute()
    origin.mkdir(exist_ok=True)
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(origin)


def dng_to_frictionless(fpth: pathlib.Path) -> pathlib.Path:
    (
        lookup,
        projectinfo,
        config,
        data,
        li_issues,
        doc_currentrevs,
        doc_descriptions,
        doc_issues,
        doc_distribution,
    ) = read_excel(output=False)
    fdir = fpth.parent
    fdir.mkdir(exist_ok=True)
    dng_to_package(
        lookup,
        config,
        projectinfo,
        doc_distribution,
        doc_issues,
        data,
        fdir=fdir,
    )
    return fdir / "datapackage.yaml"


def dng_to_package(
    lookup,
    config,
    projectinfo,
    df_distribution,
    df_issue,
    df_document,
    fdir: Path = pathlib.Path("test"),
):
    with set_directory(fdir):
        f_lkup, f_config, f_project, f_dist, f_issue, f_docs = (
            pathlib.Path("lookup.json"),
            pathlib.Path("config.json"),
            pathlib.Path("projectinfo.json"),
            pathlib.Path("distribution.csv"),
            pathlib.Path("issue.csv"),
            pathlib.Path("document.csv"),
        )
        f_lkup.write_text(lookup.model_dump_json(indent=4))
        f_config.write_text(json.dumps(config, indent=4))
        f_project.write_text(json.dumps(projectinfo, indent=4))
        df_distribution.to_csv(f_dist, index=None)
        df_issue.to_csv(f_issue, index=None)
        df_document.to_csv(f_docs, index=None)

        package = Package(
            name="document-issue",
            title="My Package",
            description="My Package for the Guide",
            resources=[
                Resource(path="distribution.csv"),
                Resource(path="issue.csv"),
                Resource(path="document.csv"),
                JsonResource(path="lookup.json"),
                JsonResource(path="projectinfo.json"),
                JsonResource(path="config.json"),
            ],
            # it's possible to provide all the official properties like homepage, version, etc
        )
        print(package)
        package.to_yaml("datapackage.yaml")
    print("done: dng_to_package")
