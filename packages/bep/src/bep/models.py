from pydantic import BaseModel, RootModel, computed_field
from enum import Enum
import pathlib
import csv


class RevisionTypeEnum(Enum):
    """Status codes for a document."""

    Preliminary = "P"
    Contractual = "C"


class StatusRevision(BaseModel):
    """Status of a document."""

    status_code: str
    revision_code: RevisionTypeEnum
    status_description: str
    revision_description: str
    description: str

    @computed_field
    @property
    def map_status(self) -> dict:  # noqa: D102
        x = " - "
        return {
            f"{self.status_code}_{self.revision_code.value}": (
                self.status_code
                + x
                + self.status_description
                + x
                + self.revision_code.value
                + x
                + self.revision_description
                + x
                + self.description
            ),
        }


class StatusRevisionTable(RootModel):
    root: list[StatusRevision]

    @computed_field
    @property
    def map_status(self) -> dict:  # noqa: D102
        return {x: y for z in self.root for x, y in z.map_status.items()}

def read_csv_records(fpth: pathlib.Path, model: type[BaseModel]) -> RootModel:
    """reads and validates a pydantic model."""
    li = [StatusRevision(**x) for x in list(csv.DictReader(fpth.read_text().replace("\ufeff", "").splitlines()))]
    return model(li)


# class Classification(BaseModel):
#     pass


# class Level(BaseModel):
#     pass


# class Type(BaseModel):
#     pass


# class Source(BaseModel):
#     pass
