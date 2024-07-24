from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
import document_issue_api.project_role.schemas as schemas
import document_issue_api.project_role.crud as crud
import typing as ty

from document_issue_api.database import (
    get_db,
)  # TODO: remove this dependency / make configurable

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/project_role/{project_id}/{role_id}",
    response_model=schemas.ProjectRoleGet,
    tags=["Project Role"],
    summary="Post Project Role.",
)
def post_project_role(
    project_id: int,
    role_id: int,
    db: Session = Depends(get_db),
    person_id: ty.Optional[int] = None,
):
    try:
        db_ = crud.post_project_role(db=db, project_id=project_id, role_id=role_id, person_id=person_id)
        db.commit()
        return db_
    except Exception as err:
        db.rollback()
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to add Project Role.\n{err}")


@router.delete(
    "/project_role/{project_id}/{role_id}",
    response_model=schemas.ProjectRoleGet,
    tags=["Project Role"],
    summary="Delete Project Role.",
)
def delete_project_role(project_id: int, role_id: int, db: Session = Depends(get_db)):
    try:
        db_ = crud.delete_project_role(db=db, project_id=project_id, role_id=role_id)
        db.commit()
        return db_
    except Exception as err:
        db.rollback()
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to delete Project Role.\n{err}")


@router.get(
    "/project_roles/{project_id}/",
    response_model=schemas.ProjectRolesGet,
    tags=["Project Role"],
    summary="Get Project Roles.",
)
def get_project_roles(project_id: int, db: Session = Depends(get_db)):
    try:
        db_ = crud.get_project_roles(db=db, project_id=project_id)
        return db_
    except Exception as err:
        db.rollback()
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to get Project Roles.\n{err}")
