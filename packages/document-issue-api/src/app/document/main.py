from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
import typing as ty
import app.document.schemas as schemas
import app.document.crud as crud

from app.database import get_db  # TODO: remove this dependency / make configurable

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/document/",
    response_model=schemas.DocumentBasePost,
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
    document_id: int, document: schemas.DocumentBasePatch, db: Session = Depends(get_db)
):
    try:
        db_ = crud.patch_document(db=db, document_id=document_id, document=document)
        db.commit()
        return db_
    except Exception as err:
        db.rollback()
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to patch Document.\n{err}")
