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


@router.get(
    "/role/{role_id}",
    response_model=schemas.RoleGet,
    tags=["Role"],
    summary="Get Role.",
)
def get_role(role_id, db: Session = Depends(get_db)):
    try:
        db_ = crud.get_role(db=db, role_id=int(role_id))
        if db_ is None:
            raise HTTPException(status_code=404, detail=f"Role {role_id} not found.")
        return db_
    except Exception as err:
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to get Role.\n{err}")


@router.get(
    "/roles",
    response_model=list[schemas.RoleGet],
    tags=["Role"],
    summary="Get Roles.",
)
def get_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        db_ = crud.get_roles(db=db, skip=skip, limit=limit)
        return db_
    except Exception as err:
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to get Roles.\n{err}")


@router.patch(
    "/role/{role_id}",
    response_model=schemas.RoleGet,
    tags=["Role"],
    summary="Patch Role.",
)
def patch_role(role_id, role: schemas.RolePatch, db: Session = Depends(get_db)):
    try:
        db_ = crud.patch_role(db=db, role_id=role_id, role=role)
        db.commit()
        return db_
    except Exception as err:
        db.rollback()
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to patch Role.\n{err}")


@router.delete(
    "/role/{role_id}",
    response_model=schemas.RoleGet,
    tags=["Role"],
    summary="Delete Role.",
)
def delete_role(role_id, db: Session = Depends(get_db)):
    try:
        db_ = crud.delete_role(db=db, role_id=role_id)
        return db_
    except Exception as err:
        db.rollback()
        logger.exception(err)
        raise HTTPException(status_code=404, detail=f"Failed to delete Role.\n{err}")
