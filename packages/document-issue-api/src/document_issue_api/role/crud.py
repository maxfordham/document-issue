import logging
from sqlalchemy.orm import Session
import app.role.schemas as schemas
import app.models as models
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

    db_ = models.Role(**role.dict())
    db.add(db_)
    db.commit()
    db.refresh(db_)
    return db_
