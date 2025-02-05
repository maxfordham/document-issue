import typing as ty

from pydantic import BaseModel


class CodeDefinitions(BaseModel):
    code: str
    description: str
    # regex: str
    nesting_charactor: ty.Optional[str] = None


class Project(CodeDefinitions):
    number: int


class Originator(CodeDefinitions):
    pass


class FunctionalBreakdown(CodeDefinitions):  # BS EN 19650 2021 addendum
    pass


class Level(CodeDefinitions):
    pass


class Volume(CodeDefinitions):
    pass


# class SpatialBreakdown(CodeDefinitions): # BS EN 19650 2021 addendum. maintain Level and Volume
#     pass


class InformationType(CodeDefinitions):  # Form
    pass


class Classification(CodeDefinitions):  # Discipline
    pass
