from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
import app.project_role.schemas as schemas
import app.project_role.crud as crud
import typing as ty

from app.database import get_db  # TODO: remove this dependency / make configurable

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/project_role/{project_id}/{role_id}",
    response_model=schemas.ProjectRoleGet,
    tags=["ProjectRole"],
    summary="Post ProjectRole.",
)
def post_project_role(project_id: int, role_id: int, db: Session = Depends(get_db)):
    try:
        db_ = crud.post_project_role(db=db, project_id=project_id, role_id=role_id)
        db.commit()
        return db_
    except Exception as err:
        db.rollback()
        logger.exception(err)
        raise HTTPException(
            status_code=404, detail=f"Failed to add ProjectRole.\n{err}"
        )
