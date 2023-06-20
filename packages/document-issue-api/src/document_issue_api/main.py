from fastapi import Depends, HTTPException
from fastapi import FastAPI
import logging
from sqlalchemy.orm import Session
from fastapi import FastAPI


import document_issue_api.issue.main as issue_main
import document_issue_api.role.main as role_main
import document_issue_api.project.main as project_main
import document_issue_api.project_role.main as project_role_main
import document_issue_api.document.main as document_main

logger = logging.getLogger(__name__)


description = "blah blah blah"
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
document_issue_api.include_router(issue_main.router)
document_issue_api.include_router(role_main.router)
document_issue_api.include_router(project_main.router)
document_issue_api.include_router(project_role_main.router)
document_issue_api.include_router(document_main.router)
