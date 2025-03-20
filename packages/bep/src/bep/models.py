"""Models for the BEP package."""
from __future__ import annotations
import csv
import pathlib
from enum import Enum

from pydantic import BaseModel, RootModel, computed_field


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


def read_csv_records(fpth: pathlib.Path | str, model: type[RootModel]) -> RootModel:
    """Read and validate a pydantic model from filepath or from csv string."""
    s = fpth.read_text().replace("\ufeff", "") if isinstance(fpth, pathlib.Path) else fpth
    return model(list(csv.DictReader(s.splitlines())))


class ProjectRole(BaseModel):
    """Project Role model."""

    role_name: str
    role_title: str
    role_category: str

class ProjectRoleTable(RootModel):
    root: list[ProjectRole]

    @computed_field
    @property
    def map_project_roles(self) -> dict:  # noqa: D102
        return {x.role_name: x.role_title for x in self.root}

# class Classification(BaseModel):
#     pass


# class Level(BaseModel):
#     pass


# class Type(BaseModel):
#     pass


# class Source(BaseModel):
#     pass
