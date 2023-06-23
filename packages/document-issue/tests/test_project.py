from document_issue.project import ProjectBase
from obj_funcs import create_project_base


def test_ProjectBase():
    proj = create_project_base()
    assert proj.project_number == 6667
