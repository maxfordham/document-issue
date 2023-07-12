from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
import document_issue_api.issue.schemas as schemas
import document_issue_api.issue.crud as crud

from document_issue_api.database import get_db  # TODO: remove this dependency / make configurable

router = APIRouter()
logger = logging.getLogger(__name__)


# ---------- /issue/ -------------------
@router.post(
    "/issue/{document_id}",
    response_model=schemas.IssueBasePost,
    tags=["Issue"],
    summary="Post Issue.",
)
def post_issue(issue: schemas.IssueBasePost, document_id, db: Session = Depends(get_db)):
    try:
        db_ = crud.post_issue(db, document_id, issue)
        db.commit()
        return db_
    except Exception as err:
        db.rollback()
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to add Issue.\n{err}")
