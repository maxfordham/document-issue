import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from document_issue_api.database import (
    get_db,
)  # TODO: remove this dependency / make configurable
from document_issue_api.document_role import crud, schemas

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/document_role/{document_id}/{role_id}",
    response_model=schemas.ProjectRoleGet,
    tags=["Document Role"],
    summary="Post Document Role.",
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
        raise HTTPException(
            status_code=404,
            detail=f"Failed to add Document Role.\n{err}",
        )


@router.get(
    "/document_roles/{document_id}/",
    response_model=list[schemas.ProjectRoleGet],
    tags=["Document Role"],
    summary="Get Document Roles.",
)
def get_document_roles(document_id: int, db: Session = Depends(get_db)):
    try:
        db_ = crud.get_document_roles(db=db, document_id=document_id)
        return db_
    except Exception as err:
        db.rollback()
        logger.exception(err)
        raise HTTPException(
            status_code=404,
            detail=f"Failed to get Document Roles.\n{err}",
        )


@router.delete(
    "/document_role/{document_id}/{role_id}",
    response_model=schemas.ProjectRoleGet,
    tags=["Document Role"],
    summary="Delete Document Role.",
)
def delete_document_role(document_id: int, role_id: int, db: Session = Depends(get_db)):
    try:
        db_ = crud.delete_document_role(db=db, document_id=document_id, role_id=role_id)
        db.commit()
        return db_
    except Exception as err:
        db.rollback()
        logger.exception(err)
        raise HTTPException(
            status_code=404,
            detail=f"Failed to delete Document Role.\n{err}",
        )
