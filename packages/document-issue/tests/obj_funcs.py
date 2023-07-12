from document_issue.project import ProjectBase


def create_project() -> ProjectBase:
    return ProjectBase(project_name="In House App Testing", project_number=6667)
