import logging
import typing as ty

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from document_issue_api.database import (
    get_db,
)  # TODO: remove this dependency / make configurable
from document_issue_api.document import crud, schemas

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/document/",
    response_model=schemas.DocumentBaseGet,
    tags=["Document"],
    summary="Post Document.",
)
def post_document(document: schemas.DocumentBasePost, db: Session = Depends(get_db)):
    try:
        db_ = crud.post_document(db=db, document=document)
        db.commit()
        return db_
    except Exception as err:
        db.rollback()
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to add Document.\n{err}")


@router.get(
    "/document/{document_id}",
    response_model=schemas.DocumentBaseGet,
    tags=["Document"],
    summary="Get Document.",
)
def get_document(document_id: int, db: Session = Depends(get_db)):
    try:
        db_ = crud.get_document(db=db, document_id=document_id)
        return db_
    except Exception as err:
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to get Document.\n{err}")


@router.get(  # NOTE: this is a duplicate of the above. but it's a different response_model
    "/document_issue/{document_id}",
    response_model=schemas.DocumentIssueGet,
    tags=["Document Issue"],
    summary="Get Document Issue.",
)
def get_document_issue(document_id: int, db: Session = Depends(get_db)):
    try:
        d_i = crud.get_document_issue(db=db, document_id=document_id)
        return d_i
    except Exception as err:
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to get Document.\n{err}")


@router.get(
    "/documents/",
    response_model=ty.List[schemas.DocumentBaseGet],
    tags=["Document"],
    summary="Get Documents.",
)
def get_documents(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    try:
        db_ = crud.get_documents(db=db, skip=skip, limit=limit)
        return db_
    except Exception as err:
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to get Documents.\n{err}")


@router.patch(
    "/document/{document_id}",
    response_model=schemas.DocumentBaseGet,
    tags=["Document"],
    summary="Patch Document.",
)
def patch_document(
    document_id: int, document: schemas.DocumentBasePatch, db: Session = Depends(get_db),
):
    try:
        db_ = crud.patch_document(db=db, document_id=document_id, document=document)
        db.commit()
        return db_
    except Exception as err:
        db.rollback()
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to patch Document.\n{err}")


@router.delete(
    "/document/{document_id}",
    response_model=schemas.DocumentBaseGet,
    tags=["Document"],
    summary="Delete Document.",
)
def delete_document(document_id: int, db: Session = Depends(get_db)):
    try:
        db_ = crud.delete_document(db=db, document_id=document_id)
        return db_
    except Exception as err:
        db.rollback()
        logger.exception(err)
        raise HTTPException(
            status_code=404, detail=f"Failed to delete Document.\n{err}",
        )
