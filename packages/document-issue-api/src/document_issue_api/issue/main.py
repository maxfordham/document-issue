from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
import app.issue.schemas as schemas
import app.issue.crud as crud

from app.database import get_db  # TODO: remove this dependency / make configurable

router = APIRouter()
logger = logging.getLogger(__name__)


# ---------- /issue/ -------------------
@router.post(
    "/issue/",
    response_model=schemas.IssueBasePost,
    tags=["Issue"],
    summary="Post Issue.",
)
def post_issue(issue: schemas.IssueBasePost, db: Session = Depends(get_db)):
    try:
        db_ = crud.post_issue(db=db, issue=issue)
        db.commit()
        return db_
    except Exception as err:
        db.rollback()
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to add Issue.\n{err}")
