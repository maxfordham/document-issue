# mapping tables
from typing import Any, List
import typing as ty
from typing_extensions import Annotated
from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator
import stringcase
import re
import xlwings as xw

from constants import DRWG_CLASSIFICATION_CODE_REGEX, UNICLASS_CLASSIFICATION_CODE_REGEX


DrwgClassificationCode = Annotated[
    str,
    AfterValidator(lambda s: re.match(DRWG_CLASSIFICATION_CODE_REGEX, s)) is not None,
]
UniclassClassificationCode = Annotated[
    str,
    AfterValidator(lambda s: re.match(DRWG_CLASSIFICATION_CODE_REGEX, s)) is not None,
]

from typing import Annotated, Hashable, List, TypeVar
from typing import Optional
from pydantic_core import PydanticCustomError
from pydantic import AfterValidator, Field, ValidationError
from pydantic.type_adapter import TypeAdapter
import enum

T = TypeVar("T", bound=Hashable)

# class DocumentCodesRegex(BaseModel):
#     project: str = DRWG_CLASSIFICATION_CODE_REGEX
#     originator: str = r"^.*$"
#     classification: str = r"^.*$"
#     info_type: str = r"^.*$"
#     drwg_type: str = r"^.*$"
#     volume: str = r"^.*$"
#     level: str = r"^.*$"
#     sequence: str = r"^.*$"
#
# class DocumentCodesExtraRegex(BaseModel):
#     classification_uniclass: str =  UNICLASS_CLASSIFICATION_CODE_REGEX
#     classification_role: str = r"^.*$"
#
# NOTE: ^ maybe regex not req. as we are using enums


def _validate_unique_list(v: list[T]) -> list[T]:
    if len(v) != len(set(v)):
        raise PydanticCustomError("unique_list", "List must be unique")
    return v


UniqueList = Annotated[
    List[T],
    AfterValidator(_validate_unique_list),
    Field(json_schema_extra={"uniqueItems": True}),
]


class DocumentCodeParts(enum.Enum):
    project: str = "project"
    originator: str = "originator"
    role: str = "role"
    classification: str = "classification"
    type: str = "type"  # info_type
    subtype: str = "subtype"  # drwg_type
    volume: str = "volume"
    level: str = "level"
    sequence: str = "sequence"  # remove?


class DocumentCodesMap(BaseModel):  # MapDocumentCodeDescription
    project: dict[str, str]
    originator: dict[ty.Literal["MXF"], ty.Literal["Max Fordham LLP"]]
    # role: dict[str, str]
    classification: dict[str, str]
    type: dict[str, str]
    # drwg_type: dict[int, str]  # info_sub_type
    volume: dict[str, str]
    level: dict[str, str]
    type_sequences: Optional[dict[str, dict[str, str]]] = None  # info_type_sequences

    nested_codes: dict[DocumentCodeParts, tuple[str]] = {
        "classification": ("role", "subrole"),
        "type": ("type", "subtype"),
    }
    nested_codes_delimiter: str = "-"


class DocumentMetadataMap(BaseModel):
    scale: dict[str, str]
    size: dict[str, str]
    status: dict[str, str]
    issue_format: dict[str, str]
    doc_source: dict[str, str]
    classification_uniclass: dict[DrwgClassificationCode, UniclassClassificationCode]
    # role: dict[DrwgClassificationCode, str]
    # info_sub_type: dict[str, str]


class LookupData(DocumentCodesMap, DocumentMetadataMap):
    pass


class DocumentCodeSpec(BaseModel):
    # regex: DocumentCodesRegex
    order: UniqueList[DocumentCodeParts] = Field(
        max_length=len(DocumentCodeParts.__members__)
    )
    map_codes: DocumentCodesMap
    map_metadata: DocumentMetadataMap


class Recipient(BaseModel):
    name: str
    email: str
    role: str


class DistributionList(BaseModel):
    recipients: List[Recipient]


import pandas as pd


def index_of_value(value, sheet):
    """look for a value in the spreadsheet"""
    for i, line in enumerate(xw.sheets[sheet].range((1, 1), (200, 200)).value):
        try:
            return (i + 1, line.index(value) + 1)
        except:
            pass
    return False


def get_table_data(name: str) -> dict:
    data = (
        xw.sheets[name]
        .range(index_of_value(f"{name}_code", name))
        .options(pd.DataFrame, expand="table")
        .value
    )
    return data[f"{name}_des"].to_dict()


def get_lookup_data() -> DocumentCodesMap:  # get_lookup_data
    names = [k for k in list(DocumentCodeParts.__members__.keys()) if k != "sequence"]
    names = names + [
        stringcase.camelcase(f)
        for f in DocumentMetadataMap.model_fields.keys()
        if f not in ["classification_uniclass"]
    ]
    sheet_names = [s.name for s in xw.sheets]
    names = [n for n in names if n in sheet_names]
    data = {stringcase.snakecase(n): get_table_data(n) for n in names}

    # classification_uniclass
    name = "classification"
    df = (
        xw.sheets[name]
        .range(index_of_value(f"{name}_code", name))
        .options(pd.DataFrame, expand="table")
        .value
    )
    data[f"classification_uniclass"] = df[f"uniclass_classification"].to_dict()

    # sequence
    name = "sequence"
    type_sequences = (
        xw.sheets[name]
        .range(index_of_value(f"{name}_code", name))
        .options(pd.DataFrame, expand="table")
        .value
    )
    type_sequences = type_sequences.to_dict()
    type_sequences = {
        k: {_k: _v for _k, _v in v.items() if _v is not None}
        for k, v in type_sequences.items()
    }
    data["type_sequences"] = type_sequences
    return LookupData(**data | type_sequences)


def project_info():
    """gets the project info from the first sheet"""
    return (
        xw.sheets["readme"]
        .range(index_of_value("Job Number", "readme"))
        .options(dict, expand="table", numbers=int)
        .value
    )


def get_issues(data):
    """work out which columns are dates"""
    match_str = r"^20(\d{2}\d{2}\d{2})-.*$"  # string match date format 20YYMMDD-...
    #                                       ^ Test here: https://regex101.com/r/qH0sU7/1
    return [c for c in data.columns if re.match(match_str, c) is not None]


import os
import json
from d_i_ui import warning_messagebox

MAX_COLS_IN_PART = 30
DEFAULT_CONFIG = {
    "job_number": "4321",
    "office": "Cambridge",  # edinburgh; bristol; manchester; cambridge; london;
    "open_on_save": "False",
    "check_on_save": "True",
    "col_widths": "100,40,9",
    "max_cols_in_part": MAX_COLS_IN_PART,
    "users": [],
    "timestamps": [],
    "filepath": "",
}
CONFIG_DIR = r"J:\J4321\Data\document_issue\config"


def verify_config(config):
    for k in DEFAULT_CONFIG.keys():
        if k not in config:
            config[k] = DEFAULT_CONFIG[k]
    return config


def config_filename(job_number):
    """return the filename of the config files."""
    # username = os.environ['username']
    return CONFIG_DIR + "\\" + str(job_number) + ".json"


def user_config(job_number):
    """loads the user configuration"""
    file = config_filename(job_number)
    try:
        if os.path.isfile(file):
            with open(file, "r") as handle:
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
    """extract data from spreadsheet and convert it to a pandas dataframe"""
    if index_of_value("Document Number", "1. Document Numbering"):
        res = (
            xw.sheets["1. Document Numbering"]
            .range(index_of_value("Sort By Uniclass", "1. Document Numbering"))
            .options(pd.Series, expand="table")
            .value
        )
        res = (
            res.reset_index(drop=False)
            .set_index("Document Number")
            .rename(columns={"Sort By Uniclass": "uniclass"})
        )
        if (
            "Document Number" not in res.columns
        ):  # backwards compatability for spreadsheet upgrade.
            res.index.names = ["Document Number Index"]
            res["Document Number"] = res.index

        if type(res) is pd.core.frame.Series:
            raise ValueError(
                "Atleast two documents required.\nOnly need one? Just add a dummy one"
            )
        if "Document Number" not in res.columns:
            res["Document Number"] = res.index
        res = res[res["Document Number"] != -2146826246]
        cols_to_remove = list(set(res.columns).intersection(map(str, range(0, 999))))
        cols_to_remove += [
            x
            for x in res.columns
            if "Column" in x or "blank" in x or "→" in x or "?" in x or "Add to " in x
        ]
        res = res.sort_values("Document Number")
        res = res.dropna(subset=["Document Number"])
        pd.options.display.float_format = "{:,.0f}".format
        return res.drop(cols_to_remove, axis=1)  # remove column that are empty.
    raise Exception(
        "Cannot Revision Information - Something has gone wrong contact support."
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
                "Atleast two people in distribution required.\nOnly need one? Just add a dummy one"
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
        'Cannot Find Distribution Table - ensure First Column is titled "Name"'
    )


def read_excel():
    lookup = get_lookup_data()
    projectinfo = project_info()
    config = user_config(projectinfo.get("Job Number"))  # define this in the UI
    data = get_pandas_data()
    li_issues = get_issues(data)
    doc_revs = data["Current Rev"].to_dict()
    doc_descriptions = data[
        [c for c in data.columns if c not in li_issues + ["Current Rev"]]
    ].T.to_dict()
    doc_issues = data[li_issues].T.to_dict()
    dist_data = get_distribution_data(li_issues=li_issues)
    print("data loaded")
    return (
        lookup,
        projectinfo,
        config,
        data,
        li_issues,
        doc_revs,
        doc_descriptions,
        doc_issues,
        dist_data,
    )
