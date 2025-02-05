import enum
import logging
import re
import typing as ty
from typing import Annotated, List, TypeVar

from pydantic import AfterValidator, BaseModel, Field
from pydantic_core import PydanticCustomError

logger = logging.getLogger(__name__)

DRWG_CLASSIFICATION_CODE_REGEX = r"^[A-Z]{1}-[0-9]{2}$"  # TODO: make configurable on a project basis
UNICLASS_CLASSIFICATION_CODE_REGEX = r"^.*$"  # TODO

DrwgClassificationCode = Annotated[
    str,
    AfterValidator(lambda s: re.match(DRWG_CLASSIFICATION_CODE_REGEX, s)) is not None,
]
UniclassClassificationCode = Annotated[
    str,
    AfterValidator(lambda s: re.match(DRWG_CLASSIFICATION_CODE_REGEX, s)) is not None,
]
T = TypeVar("T", bound=ty.Hashable)

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
    # originator: dict[str, str]
    originator: dict[
        str,  # ty.Literal["MXF"], # NOTE: relaxed MXF req. due to legacy data: 6372
        ty.Literal["Max Fordham LLP", "Max Fordham"],
    ]
    # role: dict[str, str]
    classification: dict[str, str]
    type: dict[str, str]
    # drwg_type: dict[int, str]  # info_sub_type
    volume: dict[str, str]
    level: dict[str, str]
    type_sequences: ty.Optional[dict[str, dict[str, str]]] = None  # info_type_sequences

    nested_codes: dict[DocumentCodeParts, list[str]] = {
        "classification": ["role", "subrole"],
        "type": ["type", "subtype"],
    }
    nested_codes_delimiter: str = "-"

    # @field_validator("originator")
    # def validate_originator(cls, v):
    #     if v != {"MXF": "Max Fordham LLP"}:
    #         raise logger.error(
    #             "originator must be either 'Max Fordham LLP' or 'Max Fordham'"
    #         )
    #     return {"MXF": "Max Fordham LLP"}


class DocumentMetadataMap(BaseModel):
    scale: dict[str, str]
    size: dict[str, str]
    status: dict[str, str]
    issue_format: dict[str, str]
    doc_source: dict[str, str]
    classification_uniclass: dict[
        str,
        UniclassClassificationCode,
    ]  # DrwgClassificationCode
    # role: dict[DrwgClassificationCode, str]
    # info_sub_type: dict[str, str]


class LookupData(DocumentCodesMap, DocumentMetadataMap):  # Map
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
