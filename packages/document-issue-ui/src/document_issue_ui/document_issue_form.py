# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

from document_issue.document_issue import DocumentIssue, Issue
from ipyautoui.autoobject import AutoObjectForm
import traitlets as tr
from ipyautoui.custom.editgrid import EditGrid, DataHandler
from pydantic import BaseModel, Field, RootModel, field_validator
import typing as ty
from typing import Union, Type, Optional, Callable, Any
import ipywidgets as w
from datetime import date


# + endofcell="--"
class IssueHistory(RootModel):
    root: list[Issue]


class IssueForm(AutoObjectForm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = Issue
        self._set_validate_value(self.value)
        display_bn_shownull = False


class IssueGrid(EditGrid):
    def __init__(
        self,
        schema: Union[dict, Type[BaseModel]] = None,
        value: Optional[list[dict[str, Any]]] = None,
        by_alias: bool = False,
        by_title: bool = True,
        datahandler: Optional[DataHandler] = None,
        ui_add: Optional[Callable] = None,
        ui_edit: Optional[Callable] = None,
        ui_delete: Optional[Callable] = None,
        ui_copy: Optional[Callable] = None,
        warn_on_delete: bool = False,
        show_copy_dialogue: bool = False,
        close_crud_dialogue_on_action: bool = False,
        title: str = None,
        description: str = None,
        show_title: bool = True,
        **kwargs
    ):
        kwargs["schema"] = IssueHistory
        kwargs["ui_add"] = IssueForm
        kwargs["ui_edit"] = IssueForm

        super().__init__(**kwargs)


class DocumentIssueUi(DocumentIssue):
    """metadata classifying a document and it's status within a project"""

    issue_history: ty.List[Issue] = Field(
        [],
        alias="issue",
        description="list of issues",
        json_schema_extra=dict(
            autoui="document_issue_ui.document_issue_form.IssueGrid"
        ),  # HOTFIX: # https://github.com/maxfordham/ipyautoui/issues/309
    )

    @field_validator("issue_history")
    @classmethod
    def _issue_history(cls, v):
        if len(v) == 0:
            v += [Issue(date=date.today())]
        return sorted(v, key=lambda d: d.date)


# -------------------------------------------------------------------------------------
# ^ HOTFIX: https://github.com/maxfordham/ipyautoui/issues/309
# -------------------------------------------------------------------------------------


# -

from ipyautoui.autoui import WrapSaveButtonBar, AutoUiFileMethods

class DocumentIssueForm(
    AutoObjectForm,
    WrapSaveButtonBar,
    AutoUiFileMethods,
):
    project_number = tr.Int(default_value=5001)
    map_projects = tr.Dict()  # e.g. {5003: "Default Project"}

    def _set_children(self):
        self.children = [
            self.savebuttonbar,
            w.HBox([self.bn_showraw, self.bn_shownull, self.html_title]),
            self.html_description,
            self.vbx_error,
            self.vbx_widget,
            self.vbx_showraw,
        ]
        self.show_hide_bn_nullable()

    def _post_init(self, **kwargs):
        self.di_widgets["project_number"].disabled = True
        self.di_widgets["project_name"].disabled = True
        self.order = [
            _ for _ in list(self.di_widgets.keys()) if _ != "format_configuration"
        ]
        self._project_number("change")
        self.savebuttonbar.unsaved_changes = False

    @tr.observe("project_number")
    def _project_number(self, on_change):
        self.di_widgets["project_number"].value = self.project_number
        self.di_widgets["project_name"].value = self.map_projects[self.project_number]


def get_document_issue_form(
    project_number: int, map_projects: dict, **kwargs
) -> DocumentIssueForm:
    ui = DocumentIssueForm.from_pydantic_model(
        DocumentIssueUi,
        nested_widgets=[],
        map_projects=map_projects,
        project_number=project_number,
        show_null=True,
        align_horizontal=False,
        display_bn_shownull=False,
        **kwargs
    )
    return ui


if __name__ == "__main__":
    from IPython.display import display
    import pathlib

    project_numbers = {"J5003 - Default Project": 5003, "J5001 - Test Project": 5001}
    map_projects = {v: k.split(" - ")[1] for k, v in project_numbers.items()}
    project_number = 5003
    ui = get_document_issue_form(project_number, map_projects, path=pathlib.Path("docissue.json"))
    # ui.path = pathlib.Path("docissue.json")
    display(ui)

# --


