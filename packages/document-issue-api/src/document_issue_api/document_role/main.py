from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
import document_issue_api.document_role.schemas as schemas
import document_issue_api.document_role.crud as crud
import typing as ty

from document_issue_api.database import (
    get_db,
)  # TODO: remove this dependency / make configurable

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/document_role/{document_id}/{role_id}",
    response_model=schemas.ProjectRoleGet,
    tags=["ProjectRole"],
    summary="Post ProjectRole.",
)
def post_document_role(
    document_id: int,
    role_id: int,
    db: Session = Depends(get_db),
):
    try:
        db_ = crud.post_document_role(db=db, document_id=document_id, role_id=role_id)
        db.commit()
        return db_
    except Exception as err:
        db.rollback()
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to add ProjectRole.\n{err}")


@router.get(
    "/document_roles/{document_id}/",
    response_model=list[schemas.ProjectRoleGet],
    tags=["ProjectRole"],
    summary="Get ProjectRoles.",
)
def get_document_roles(document_id: int, db: Session = Depends(get_db)):
    try:
        db_ = crud.get_document_roles(db=db, document_id=document_id)
        return db_
    except Exception as err:
        db.rollback()
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to get ProjectRoles.\n{err}")


@router.delete(
    "/document_role/{document_id}/{role_id}",
    response_model=schemas.ProjectRoleGet,
    tags=["ProjectRole"],
    summary="Delete ProjectRole.",
)
def delete_document_role(document_id: int, role_id: int, db: Session = Depends(get_db)):
    try:
        db_ = crud.delete_document_role(db=db, document_id=document_id, role_id=role_id)
        db.commit()
        return db_
    except Exception as err:
        db.rollback()
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to delete ProjectRole.\n{err}")
