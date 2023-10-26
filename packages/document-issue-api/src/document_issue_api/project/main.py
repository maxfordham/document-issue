from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
import document_issue_api.project.schemas as schemas
import document_issue_api.project.crud as crud
import typing as ty

from document_issue_api.database import (
    get_db,
)  # TODO: remove this dependency / make configurable

router = APIRouter()
logger = logging.getLogger(__name__)


# project base
@router.post(
    "/project/",
    response_model=schemas.ProjectGet,
    tags=["Project"],
    summary="Post Project.",
)
def post_project(project: schemas.ProjectPost, db: Session = Depends(get_db)):
    try:
        db_ = crud.post_project(db=db, project=project)
        db.commit()
        return db_
    except Exception as err:
        db.rollback()
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to add Project.\n{err}")


@router.get(
    "/project/{project_id}",
    response_model=schemas.ProjectGet,
    tags=["Project"],
    summary="Get Project.",
)
def get_project(project_id: int, db: Session = Depends(get_db)):
    try:
        db_ = crud.get_project(db=db, project_id=project_id)
        if db_ is None:
            raise HTTPException(
                status_code=204, detail=f"Project id ={project_id} does not exist."
            )
        else:
            return db_
    except Exception as err:
        raise HTTPException(status_code=404, detail=f"Failed to get Project.\n{err}")


@router.get(
    "/project/",
    response_model=list[schemas.ProjectGet],
    tags=["Project"],
    summary="Get Projects.",
)
def get_projects(db: Session = Depends(get_db), limit: int = 100, skip: int = 0):
    try:
        db_ = crud.get_projects(db=db, limit=limit, skip=skip)
        return db_
    except Exception as err:
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to get Projects.\n{err}")


@router.delete(
    "/project/{project_id}",
    response_model=schemas.ProjectGet,
    tags=["Project"],
    summary="Delete Project.",
)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    try:
        db_ = crud.delete_project(db=db, project_id=project_id)
        return db_
    except Exception as err:
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to delete Project.\n{err}")


@router.patch(
    "/project/{project_id}",
    response_model=schemas.ProjectGet,
    tags=["Project"],
    summary="Patch Project.",
)
def patch_project(
    project_id: int, project: schemas.ProjectPatch, db: Session = Depends(get_db)
):
    try:
        db_ = crud.patch_project(db=db, project_id=project_id, project=project)
        return db_
    except Exception as err:
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to patch Project.\n{err}")
