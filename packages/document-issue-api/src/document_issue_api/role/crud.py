import logging
from sqlalchemy.orm import Session
import document_issue_api.role.schemas as schemas
import document_issue_api.models as models
import typing as ty
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)


# role
def post_role(db: Session, role: schemas.RolePost) -> models.Role:
    """Create a new role.

    Args:
        db (Session): The session linking to the database
        role (schemas.RolePost): The role to post

    Returns:
        models.Role: The postd role
    """

    db_ = models.Role(**role.model_dump())
    db.add(db_)
    db.commit()
    db.refresh(db_)
    return db_


def get_role(db: Session, role_id: int) -> models.Role:
    """Get a role.

    Args:
        db (Session): The session linking to the database
        role_id (int): The id of the role to get

    Returns:
        models.Role: The getd role
    """
    db_ = db.get(models.Role, role_id)
    return db_


def get_roles(db: Session, skip: int = 0, limit: int = 100) -> ty.List[models.Role]:
    """Get all roles.

    Args:
        db (Session): The session linking to the database
        skip (int, optional): The number of roles to skip. Defaults to 0.
        limit (int, optional): The number of roles to return. Defaults to 100.

    Returns:
        ty.List[models.Role]: The getd roles
    """

    db_ = db.query(models.Role).offset(skip).limit(limit).all()
    return db_


def patch_role(db: Session, role_id: int, role: schemas.RolePatch) -> models.Role:
    """Patch a role.

    Args:
        db (Session): The session linking to the database
        role_id (int): The id of the role to patch
        role (schemas.RolePatch): The role patch

    Returns:
        models.Role: The patched role
    """

    db_ = db.get(models.Role, role_id)
    role_data = jsonable_encoder(db_)
    update_data = role.model_dump(exclude_unset=True)
    for field in role_data:
        if field in update_data:
            setattr(db_, field, update_data[field])
    db.commit()
    db.refresh(db_)
    return db_


def delete_role(db: Session, role_id: int) -> models.Role:
    """Delete a role.

    Args:
        db (Session): The session linking to the database
        role_id (int): The id of the role to delete

    Returns:
        models.Role: The deleted role
    """

    db_ = db.get(models.Role, role_id)
    db.delete(db_)
    db.commit()
    return db_
