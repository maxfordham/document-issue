import logging
from sqlalchemy.orm import Session
import document_issue_api.project_role.schemas as schemas
import document_issue_api.models as models
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


def get_project_roles(db: Session, project_id: int) -> schemas.ProjectRolesGet:
    """Get all project roles.

    Args:
        db (Session): The session linking to the database
        project_id (int): The ID of the project

    Returns:
        models.ProjectRole: The project role
    """
    db_ = (
        db.query(models.ProjectRole)
        .filter(models.ProjectRole.project_id == project_id)
        .all()
    )
    roles = [_.role for _ in db_]
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    return schemas.ProjectRolesGet(project=project, roles=roles)


def delete_project_role(
    db: Session, project_id: int, role_id: int
) -> schemas.ProjectRoleGet:
    """Delete a project role.

    Args:
        db (Session): The session linking to the database
        project_id (int): The ID of the project
        role_id (int): The ID of the role

    Returns:
        models.ProjectRole: The deleted project role
    """
    db_ = (
        db.query(models.ProjectRole)
        .filter(models.ProjectRole.project_id == project_id)
        .filter(models.ProjectRole.role_id == role_id)
        .first()
    )
    _ = schemas.ProjectRoleGet.from_orm(db_)
    db.delete(db_)
    return _