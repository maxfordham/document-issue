from fastapi import Depends, HTTPException
from fastapi import FastAPI
import logging
from sqlalchemy.orm import Session
from fastapi import FastAPI


import document_issue_api.issue.main as issue_main
import document_issue_api.role.main as role_main
import document_issue_api.project.main as project_main
import document_issue_api.project_role.main as project_role_main
import document_issue_api.document_role.main as document_role_main
import document_issue_api.document.main as document_main
import document_issue_api.person.main as person_main

logger = logging.getLogger(__name__)


description = """API and database for managing document issue and revision control
 within the AEC Industry."""
app = FastAPI(
    # openapi_tags=tags_metadata,
    title="document-issue",
    description=description,
    version="0.3.0",  # _version.get_versions()["version"],
    # terms_of_service="http://example.com/terms/",
    contact={
        "name": "John Gunstone",
        "email": "j.gunstone@maxfordham.com",
    },
    # license_info={
    #     "name": "",
    #     "url": "",
    # },
)
app.include_router(project_main.router)
app.include_router(person_main.router)
app.include_router(role_main.router)
app.include_router(issue_main.router)
app.include_router(document_main.router)
app.include_router(project_role_main.router)
app.include_router(document_role_main.router)
