import logging
from sqlalchemy.orm import Session
import app.project_role.schemas as schemas
import app.models as models
import typing as ty
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)


def post_project_role(db: Session, project_id: int, role_id: int) -> models.ProjectRole:
    """Create a new project role.

    Args:
        db (Session): The session linking to the database
        project_id (int): The ID of the project
        role_id (int): The ID of the role

    Returns:
        models.ProjectRole: The posted project role
    """

    db_ = models.ProjectRole(project_id=project_id, role_id=role_id)
    db.add(db_)
    db.commit()
    db.refresh(db_)
    return db_


def get_project_role(
    db: Session, project_id: int, role_id: ty.Optional[int] = None
) -> list[models.ProjectRole]:
    """Get a project role by ID.

    Args:
        db (Session): The session linking to the database
        project_id (int): The ID of the project
        role_id (int, optional): The ID of the role. Defaults to None.

    Returns:
        models.ProjectRole: The project role
    """
    db_ = db.query(models.ProjectRole).filter(
        models.ProjectRole.project_id == project_id
    )
    if role_id is not None:
        db_ = db_.filter(models.ProjectRole.role_id == role_id).all()
    else:
        db_ = db_.all()
    return db_
