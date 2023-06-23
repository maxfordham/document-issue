from document_issue.project import ProjectBase
from obj_funcs import create_project


def test_ProjectBase():
    proj = create_project()
    assert proj.project_number == 6667
