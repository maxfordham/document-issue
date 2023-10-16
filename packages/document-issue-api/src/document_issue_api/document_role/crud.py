import logging
from sqlalchemy.orm import Session
import document_issue_api.document_role.schemas as schemas
import document_issue_api.models as models
import typing as ty
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)


def post_document_role(db: Session, role_id: int, document_id: int) -> schemas.ProjectRoleGet:
    """Create a new project role.

    Args:
        db (Session): The session linking to the database
        project_id (int): The ID of the project
        role_id (int): The ID of the role

    Returns:
        models.DocumentRole: The posted project role
    """
    db_ = models.DocumentRole(role_id=role_id, document_id=document_id)
    db.add(db_)
    db.commit()
    db.refresh(db_)
    return schemas.ProjectRoleGet.model_validate(db_.role.project_role[0])


def get_document_roles(db: Session, document_id: int) -> ty.List[schemas.ProjectRoleGet]:
    """Get all project roles.

    Args:
        db (Session): The session linking to the database
        project_id (int): The ID of the project

    Returns:
        models.DocumentRole: The project role
    """
    db_ = db.query(models.DocumentRole).filter(models.DocumentRole.document_id == document_id).all()
    return [schemas.ProjectRoleGet.model_validate(_.role.project_role[0]) for _ in db_]


def delete_document_role(db: Session, role_id: int, document_id: int) -> schemas.ProjectRoleGet:
    """Delete a project role.

    Args:
        db (Session): The session linking to the database
        project_id (int): The ID of the project
        role_id (int): The ID of the role

    Returns:
        models.DocumentRole: The deleted project role
    """
    db_ = (
        db.query(models.DocumentRole)
        .filter(models.DocumentRole.document_id == document_id)
        .filter(models.DocumentRole.role_id == role_id)
        .first()
    )
    db.delete(db_)
    return schemas.ProjectRoleGet.model_validate(db_.role.project_role[0])
