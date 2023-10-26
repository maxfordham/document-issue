import logging
from sqlalchemy.orm import Session
import document_issue_api.project.schemas as schemas
import document_issue_api.models as models
import typing as ty
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)


def post_project(db: Session, project: schemas.ProjectPost) -> models.Project:
    """Create a new project.

    Args:
        db (Session): The session linking to the database
        project (schemas.ProjectPost): The project to post

    Returns:
        models.Project: The postd project
    """

    db_ = models.Project(**project.model_dump())
    db.add(db_)
    db.commit()
    db.refresh(db_)
    return db_


def get_project(db: Session, project_id: int) -> models.Project:
    """Get a project by ID.

    Args:
        db (Session): The session linking to the database
        project_id (int): The ID of the project to get

    Returns:
        models.Project: The project
    """

    db_ = db.query(models.Project).filter(models.Project.id == project_id).first()
    return db_


def get_projects(
    db: Session, limit: int = 100, skip: int = 0
) -> ty.List[models.Project]:
    """Get all projects.

    Args:
        db (Session): The session linking to the database
        limit (int, optional): The maximum number of projects to return. Defaults to 100.
        skip (int, optional): The number of projects to skip. Defaults to 0.

    Returns:
        ty.List[models.Project]: The list of projects
    """

    db_ = db.query(models.Project).offset(skip).limit(limit).all()
    return db_


def delete_project(db: Session, project_id: int) -> models.Project:
    """Delete a project by ID.

    Args:
        db (Session): The session linking to the database
        project_id (int): The ID of the project to delete

    Returns:
        models.Project: The deleted project
    """

    db_ = db.query(models.Project).filter(models.Project.id == project_id).first()
    db.delete(db_)
    db.commit()
    return db_


def patch_project(
    db: Session, project_id: int, project: schemas.ProjectPatch
) -> models.Project:
    """Patch a project by ID.

    Args:
        db (Session): The session linking to the database
        project (schemas.ProjectPatch): The project to patch

    Returns:
        models.Project: The patched project
    """

    db_ = db.query(models.Project).filter(models.Project.id == project_id).first()
    update_data = project.model_dump(exclude_unset=True)
    for field in jsonable_encoder(db_):
        if field in update_data:
            setattr(db_, field, update_data[field])
    db.add(db_)
    db.commit()
    db.refresh(db_)
    return db_
