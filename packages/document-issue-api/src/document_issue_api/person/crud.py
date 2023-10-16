import logging
from sqlalchemy.orm import Session
import document_issue_api.person.schemas as schemas
import document_issue_api.models as models
import typing as ty
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)


# role
def post_person(db: Session, person: schemas.PersonPost) -> models.Role:
    """Create a new role.

    Args:
        db (Session): The session linking to the database
        role (schemas.RolePost): The role to post

    Returns:
        models.Role: The postd role
    """

    db_ = models.Person(**person.model_dump())
    db.add(db_)
    db.commit()
    db.refresh(db_)
    return db_


def get_person(db: Session, person_id: int) -> models.Person:
    """Get a role by ID.

    Args:
        db (Session): The session linking to the database
        role_id (int): The ID of the role to get

    Returns:
        models.Role: The role
    """

    db_ = db.query(models.Person).filter(models.Person.id == person_id).first()
    return db_


def get_people(db: Session, limit: int = 100, skip: int = 0) -> ty.List[models.Person]:
    """Get all roles.

    Args:
        db (Session): The session linking to the database
        limit (int, optional): The maximum number of roles to return. Defaults to 100.
        skip (int, optional): The number of roles to skip. Defaults to 0.

    Returns:
        ty.List[models.Role]: The list of roles
    """

    db_ = db.query(models.Person).offset(skip).limit(limit).all()
    return db_


def delete_person(db: Session, person_id: int) -> models.Person:
    """Delete a role by ID.

    Args:
        db (Session): The session linking to the database
        role_id (int): The ID of the role to delete

    Returns:
        models.Role: The deleted role
    """

    db_ = db.query(models.Person).filter(models.Person.id == person_id).first()
    db.delete(db_)
    db.commit()
    return db_


def patch_person(db: Session, person_id: int, person: schemas.PersonPatch) -> models.Person:
    """Patch a person by ID.

    Args:
        db (Session): The session linking to the database
        person_id (int): The ID of the person to patch
        person (schemas.RolePatch): The person to patch

    Returns:
        models.Role: The patched person
    """

    db_ = db.query(models.Person).filter(models.Person.id == person_id).first()
    person_data = jsonable_encoder(db_)
    update_data = person.dict(exclude_unset=True)
    for field in person_data:
        if field in update_data:
            setattr(db_, field, update_data[field])
    db.add(db_)
    db.commit()
    db.refresh(db_)
    return db_
