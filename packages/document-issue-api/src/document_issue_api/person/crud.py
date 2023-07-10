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

    db_ = models.Person(**person.dict())
    db.add(db_)
    db.commit()
    db.refresh(db_)
    return db_
