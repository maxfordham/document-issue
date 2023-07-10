from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
import document_issue_api.person.schemas as schemas
import document_issue_api.person.crud as crud

from document_issue_api.database import (
    get_db,
)  # TODO: remove this dependency / make configurable

router = APIRouter()
logger = logging.getLogger(__name__)


# ---------- /person/ -------------------
@router.post(
    "/person/",
    response_model=schemas.PersonGet,
    tags=["Person"],
    summary="Post Person.",
)
def post_person(person: schemas.PersonPost, db: Session = Depends(get_db)):
    try:
        db_ = crud.post_person(db=db, person=person)
        db.commit()
        return db_
    except Exception as err:
        db.rollback()
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to add Role.\n{err}")
