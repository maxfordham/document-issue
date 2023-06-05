from fastapi import Depends, HTTPException
from fastapi import FastAPI
import logging
from sqlalchemy.orm import Session
from fastapi import FastAPI


import app.issue.main as issue_main
import app.role.main as role_main
import app.project.main as project_main
import app.project_role.main as project_role_main

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
app.include_router(issue_main.router)
app.include_router(role_main.router)
app.include_router(project_main.router)
app.include_router(project_role_main.router)
