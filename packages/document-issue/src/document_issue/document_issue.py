import typing as ty
from typing import Annotated

from pydantic import (
    AfterValidator,
    BeforeValidator,
    Field,
)
from tabulate import tabulate

from document_issue.codes import (
    Classification,
    FunctionalBreakdown,
    InformationType,
    Level,
    Originator,
    Project,
    Volume,
)
from document_issue.document import Document
from document_issue.enums import RoleEnum
from document_issue.issue import Issue
from document_issue.project import ProjectBase
from document_issue.role import DocumentRole

# ------------------------------------------------------------------------------------------
# NOTE: the DocumentIssue shown here is the ideal output presentation for a single document.
#       it is not the closest representation of what is in the database. The data will need
#       reshaping out of the DB to create the format below.
# ------------------------------------------------------------------------------------------


def document_role_before(v: ty.List) -> ty.List:
    if len(v) == 0:
        v = [DocumentRole(role=RoleEnum.director, initials="DR")]
    else:
        pass
    return v


def document_role_after(v: ty.List[DocumentRole]) -> ty.List[DocumentRole]:
    if len(v) > 0:
        if v[0].role_name != RoleEnum.director:
            if v[0].role_name != "Director in Charge":
                v = [DocumentRole(role=RoleEnum.director, initials="DR")] + v
    else:
        pass
    return v


class DocumentIssue(Document, ProjectBase):
    """metadata classifying a document and it's status within a project"""

    document_role: Annotated[
        ty.List[DocumentRole],
        BeforeValidator(document_role_before),
        AfterValidator(document_role_after),
    ] = Field(
        [],
        alias="roles",  # TODO: make validation alias
        min_length=1,
        description="indicates people responsible for this document",
        validate_default=True,
    )
    issue_history: ty.List[Issue] = Field(
        [],
        alias="issue",  # TODO: make validation alias
        description="list of issues",
        json_schema_extra=dict(format="dataframe"),
    )

    @property
    def filename(self):
        return self.document_code

    @property
    def issue_history_table(self):
        """Create the markdown grid table using tabulate"""
        # Define headers for tabulate
        headers = ["Date", "Rev", "Status", "Description", "Issue Notes"]
        if self.format_configuration.output_author:
            headers.append("Author")
            if self.format_configuration.output_checked_by:
                headers.append("Checker")

        # Create list of dicts ordered by date in descending order
        map_title_to_field = {v.title: k for k, v in Issue.model_fields.items()}
        li_issue_history = []
        for issue in sorted(self.issue_history, key=lambda d: d.date, reverse=True):
            di_issue = issue.model_dump()
            di_issue["date"] = di_issue["date"].strftime(
                self.format_configuration.date_string_format,
            )
            di_issue_with_title = {}
            for header in headers:
                if header in map_title_to_field:
                    di_issue_with_title[f"**{header}**"] = di_issue[
                        map_title_to_field[header]
                    ]
                else:
                    raise ValueError(
                        f"Header '{header}' not defined as a title in Issue schema.",
                    )
            li_issue_history.append(di_issue_with_title)

        return tabulate(
            li_issue_history,
            headers="keys",
            tablefmt="grid",
        )

    @property
    def roles_table(self):
        headers = ["Initials", "Role"]
        map_title_to_field = {v.title: k for k, v in DocumentRole.model_fields.items()}
        li_document_roles = []
        for document_role in self.document_role:
            di_document_role = document_role.model_dump(mode="json")
            di_document_role_with_title = {}
            for header in headers:
                if header in map_title_to_field:
                    di_document_role_with_title[f"**{header}**"] = di_document_role[
                        map_title_to_field[header]
                    ]
                else:
                    raise ValueError(
                        f"Header '{header}' not defined as a title in DocumentRole"
                        " schema.",
                    )
            li_document_roles.append(di_document_role_with_title)
        return tabulate(
            li_document_roles,
            headers="keys",
            tablefmt="grid",
        )

    @property
    def notes_table(self):
        li_notes = [[i + 1, note] for i, note in enumerate(self.notes)]
        return tabulate(
            li_notes,
            tablefmt="grid",
        )

    @property
    def current_issue(self) -> ty.Union[Issue, None]:
        if len(self.issue_history) > 0:
            return sorted(self.issue_history, key=lambda d: d.date, reverse=True)[0]
        return None

    @property
    def current_issue_long_date(self):
        return self.current_issue.date.strftime("%B %Y")

    @property
    def director_in_charge(self):
        for role in self.document_role:
            if (
                role.role_name == RoleEnum.director
                or role.role_name == RoleEnum.director.value
            ):
                return role.initials

    # TODO: add this validation after ensuring that a director is shown on all existing schedules
    # @field_validator("document_role")
    # @classmethod
    # def _document_role(cls, v):
    #     assert "Director in Charge" in [_.role_name.value in _ in v]
    #     return v



class DocumentIssueClassification(DocumentIssue):
    classification: Classification = Field(None)  # TODO: add classification
    # roles: ty.List[Role] #TODO add roles


class DocumentIssueV2(DocumentIssue): # allow None now... but will make these required fields eventually
    project: ty.Optional[Project] = None
    originator: ty.Optional[Originator] = None
    classification: ty.Optional[Classification] = None
    information_type: ty.Optional[InformationType] = None
    functional_breakdown: ty.Optional[FunctionalBreakdown] = None
    level: ty.Optional[Level] = None
    volume: ty.Optional[Volume] = None
