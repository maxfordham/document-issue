import typing as ty
from datetime import date, datetime
from typing import Type, Union

import ipywidgets as w
import traitlets as tr
import yaml
from document_issue.document_issue import DocumentIssue, Issue
from ipyautoui.autodisplay_renderers import preview_yaml_string

# +
from ipyautoui.autoobject import AutoObjectForm
from ipyautoui.autoui import AutoUiFileMethods, WrapSaveButtonBar
from ipyautoui.custom.buttonbars import CrudOptions, CrudView
from ipyautoui.custom.editgrid import EditGrid, UiDelete
from IPython.display import clear_output
from pydantic import BaseModel, ConfigDict, Field, RootModel, field_validator

# -

HEADER_BACKGROUND_COLOUR = "rgb(207, 212, 252, 1)"


class IssueDelete(UiDelete):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def value_summary(self):
        if self.columns:
            return {k: {k_: v_ for k_, v_ in v.items() if k_ in self.columns} for k, v in self.value.items()}
        return self.value

    def _update_display(self):
        with self.out_delete:
            clear_output()
            display(
                preview_yaml_string(yaml.dump(self.value_summary)),
            )  # TODO: Move to ipyautoui https://github.com/maxfordham/ipyautoui/issues/324


BUTTONBAR_CONFIG_TYPES = CrudView(
    add=CrudOptions(
        tooltip="Add Issue",
        tooltip_clicked="Go back to table",
        button_style="success",
        message="➕ <i>Add Issue</i>",
    ),
    edit=CrudOptions(
        tooltip="Edit Selected Issue",
        tooltip_clicked="Go back to table",
        button_style="warning",
        message="✏️ <i>Edit Issue</i>",
    ),
    copy=CrudOptions(
        tooltip="Copy Selected Issues",
        tooltip_clicked="Go back to table",
        button_style="primary",
        message="📝 <i>Copy Issue</i>",
    ),
    delete=CrudOptions(
        tooltip="Delete Selected Issues",
        tooltip_clicked="Go back to table",
        button_style="danger",
        message="🗑️ <i>Delete Issue</i>",
    ),
)


# +
class IssueHistory(RootModel):
    root: list[Issue]


class IssueForm(AutoObjectForm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = Issue
        self._set_validate_value(self.value)
        display_bn_shownull = False


class IssueGrid(EditGrid):
    def __init__(self, schema: Union[dict, Type[BaseModel]] = None, **kwargs):
        kwargs["schema"] = IssueHistory
        kwargs["ui_add"] = IssueForm
        kwargs["ui_edit"] = IssueForm
        kwargs["ui_delete"] = IssueDelete
        kwargs["close_crud_dialogue_on_action"] = True
        kwargs["warn_on_delete"] = True
        kwargs["grid_style"] = {"header_background_color": HEADER_BACKGROUND_COLOUR}
        super().__init__(**kwargs)
        self.buttonbar_grid.crud_view = BUTTONBAR_CONFIG_TYPES
        self._set_date_desc()
        # HOTFIX: Be good to move save message to ipyautoui when `close_crud_dialogue_on_action` set to True
        self.ui_add.savebuttonbar.bn_save.on_click(self._show_save_message)
        self.ui_edit.savebuttonbar.bn_save.on_click(self._show_save_message)

    def _set_date_desc(self):
        if "Date" not in self.grid.data.columns:
            raise ValueError("Missing 'Date' from data.")
        column_index = list(self.grid.data.columns).index("Date") + 1
        self.grid.transform(
            [{"type": "sort", "columnIndex": column_index, "desc": True}],
        )

    def _show_save_message(self, onchange):
        self.buttonbar_grid.message.value = f"<i>changes saved: {datetime.now().strftime('%H:%M:%S')}</i>"


class DocumentIssueUi(DocumentIssue):
    """Metadata classifying a document and its status within a project"""

    issue_history: ty.List[Issue] = Field(
        [],
        alias="issue",
        description="list of issues",
        json_schema_extra=dict(
            autoui="document_issue_ui.document_issue_form.IssueGrid",
        ),  # HOTFIX: # https://github.com/maxfordham/ipyautoui/issues/309
    )

    @field_validator("issue_history")
    @classmethod
    def _issue_history(cls, v):
        if not v:
            v += [Issue(date=date.today())]
        return v

    model_config = ConfigDict(title="Document Issue")


# -------------------------------------------------------------------------------------
# ^ HOTFIX: https://github.com/maxfordham/ipyautoui/issues/309
# -------------------------------------------------------------------------------------


class DocumentIssueForm(
    AutoObjectForm,
    WrapSaveButtonBar,
    AutoUiFileMethods,
):
    project_number = tr.Int(default_value=5001)
    map_projects = tr.Dict()  # e.g. {5003: "Default Project"}

    @property
    def project_name(self):
        return self.map_projects[self.project_number]

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
        self.order = [_ for _ in list(self.di_widgets.keys()) if _ != "format_configuration"]
        self._project_number("change")
        self.savebuttonbar.unsaved_changes = False

    @tr.observe("project_number")
    def _project_number(self, on_change):
        self.di_widgets["project_number"].value = self.project_number
        self.di_widgets["project_name"].value = self.project_name


def get_document_issue_form(
    map_projects: dict,
    project_number: int = 5001,
    **kwargs,
) -> DocumentIssueForm:
    ui = DocumentIssueForm.from_pydantic_model(
        DocumentIssueUi,
        nested_widgets=[],
        map_projects=map_projects,
        project_number=project_number,
        show_null=True,
        align_horizontal=False,
        display_bn_shownull=False,
        **kwargs,
    )
    ui.di_boxes["issue_history"].widget.grid.layout.width = "1250px"  # HOTFIX: Stops grid being squashed
    ui.di_boxes["notes"].widget.layout.width = "100%"
    ui.di_boxes["document_role"].widget.layout.width = "100%"
    return ui


if __name__ == "__main__":
    import pathlib

    from IPython.display import display

    project_numbers = {"J5003 - Default Project": 5003, "J5001 - Test Project": 5001}
    map_projects = {v: k.split(" - ")[1] for k, v in project_numbers.items()}
    project_number = 5003
    ui = get_document_issue_form(
        project_number=project_number,
        map_projects=map_projects,
        path=pathlib.Path("docissue.json"),
    )
    display(ui)
# -
