from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
import document_issue_api.role.schemas as schemas
import document_issue_api.role.crud as crud

from document_issue_api.database import get_db  # TODO: remove this dependency / make configurable

router = APIRouter()
logger = logging.getLogger(__name__)


# ---------- /role/ -------------------
@router.post(
    "/role/",
    response_model=schemas.RoleGet,
    tags=["Role"],
    summary="Post Role.",
)
def post_role(role: schemas.RolePost, db: Session = Depends(get_db)):
    try:
        db_ = crud.post_role(db=db, role=role)
        db.commit()
        return db_
    except Exception as err:
        db.rollback()
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to add Role.\n{err}")
