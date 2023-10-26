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


@router.get(
    "/person/{person_id}",
    response_model=schemas.PersonGet,
    tags=["Person"],
    summary="Get Person.",
)
def get_person(person_id: int, db: Session = Depends(get_db)):
    try:
        db_ = crud.get_person(db=db, person_id=person_id)
    except Exception as err:
        raise HTTPException(status_code=404, detail=f"Failed to get Role.\n{err}")
    if db_ is None:
        raise HTTPException(
            status_code=204, detail=f"Person id ={person_id} does not exist."
        )
    else:
        return db_


@router.get(
    "/person/",
    response_model=list[schemas.PersonGet],
    tags=["Person"],
    summary="Get People.",
)
def get_people(db: Session = Depends(get_db), limit: int = 100, skip: int = 0):
    try:
        db_ = crud.get_people(db=db, limit=limit, skip=skip)
        return db_
    except Exception as err:
        raise HTTPException(status_code=404, detail=f"Failed to get People.\n{err}")


@router.patch(
    "/person/{person_id}",
    response_model=schemas.PersonGet,
    tags=["Person"],
    summary="Patch Person.",
)
def patch_person(
    person_id: int, person: schemas.PersonPatch, db: Session = Depends(get_db)
):
    try:
        db_ = crud.patch_person(db=db, person_id=person_id, person=person)
        db.commit()
        return db_
    except Exception as err:
        db.rollback()
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to patch Person.\n{err}")


@router.delete(
    "/person/{person_id}",
    response_model=schemas.PersonGet,
    tags=["Person"],
    summary="Delete Person.",
)
def delete_person(person_id: int, db: Session = Depends(get_db)):
    try:
        db_ = crud.delete_person(db=db, person_id=person_id)
        db.commit()
        return db_
    except Exception as err:
        db.rollback()
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to delete Person.\n{err}")
