import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from document_issue_api.database import (
    get_db,
)  # TODO: remove this dependency / make configurable
from document_issue_api.issue import crud, schemas

router = APIRouter()
logger = logging.getLogger(__name__)


# ---------- /issue/ -------------------
@router.post(
    "/issue/{document_id}",
    response_model=schemas.IssueBaseGet,
    tags=["Issue"],
    summary="Post an Issue onto a Document.",
)
def post_issue(
    issue: schemas.IssueBasePost, document_id, db: Session = Depends(get_db),
):
    try:
        db_ = crud.post_issue(db, document_id, issue)
        db.commit()
        return db_
    except Exception as err:
        db.rollback()
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to add Issue.\n{err}")


@router.get(
    "/issue/{issue_id}",
    response_model=schemas.IssueBaseGet,
    tags=["Issue"],
    summary="Get an Issue.",
)
def get_issue(issue_id, db: Session = Depends(get_db)):
    try:
        db_ = crud.get_issue(db, issue_id)
        if db_ is None:
            raise HTTPException(status_code=404, detail=f"Issue {issue_id} not found.")
        return db_
    except Exception as err:
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to get Issue.\n{err}")


@router.patch(
    "/issue/{issue_id}",
    response_model=schemas.IssueBaseGet,
    tags=["Issue"],
    summary="Patch an Issue.",
)
def patch_issue(issue_id, issue: schemas.IssueBasePatch, db: Session = Depends(get_db)):
    try:
        db_ = crud.patch_issue(db, issue_id, issue)
        db.commit()
        return db_
    except Exception as err:
        db.rollback()
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to patch Issue.\n{err}")


@router.delete(
    "/issue/{issue_id}",
    response_model=schemas.IssueBaseGet,
    tags=["Issue"],
    summary="Delete an Issue.",
)
def delete_issue(issue_id, db: Session = Depends(get_db)):
    try:
        db_ = crud.delete_issue(db, issue_id)
        if db_ is None:
            raise HTTPException(status_code=404, detail=f"Issue {issue_id} not found.")
        db.commit()
        return db_
    except Exception as err:
        db.rollback()
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to delete Issue.\n{err}")
