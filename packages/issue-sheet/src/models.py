from typing_extensions import Annotated
from pydantic import BaseModel
import typing as ty
from pydantic.functional_validators import AfterValidator
import re

from constants import (
    DRWG_CLASSIFICATION_CODE_REGEX,
    UNICLASS_CLASSIFICATION_CODE_REGEX,
    CONFIG_DIR,
)


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


# from document_issue.project import Project


# class ProjectInfo(Project):
#     client_name: str  # TODO: retrieve this from roles table
#     project_leader: str  # TODO: retrieve this from roles table
#     naming_convention: str  # TODO: retrieve this from lookup table


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

    nested_codes: dict[DocumentCodeParts, list[str]] = {
        "classification": ["role", "subrole"],
        "type": ["type", "subtype"],
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


# class DocumentCodeSpec(BaseModel):
#     # regex: DocumentCodesRegex
#     order: UniqueList[DocumentCodeParts] = Field(
#         max_length=len(DocumentCodeParts.__members__)
#     )
#     map_codes: DocumentCodesMap
#     map_metadata: DocumentMetadataMap


# class Recipient(BaseModel):
#     name: str
#     email: str
#     role: str


# class DistributionList(BaseModel):
#     recipients: List[Recipient]
