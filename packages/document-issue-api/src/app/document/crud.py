import logging
from sqlalchemy.orm import Session
import app.document.schemas as schemas
import app.models as models
import typing as ty
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)


def post_document(db: Session, document: schemas.DocumentBasePost) -> models.Document:
    """Create a new document.

    Args:
        db (Session): The session linking to the database
        document (schemas.DocumentBasePost): The document to post

    Returns:
        models.Document: The posted document
    """

    db_document = models.Document(**document.dict())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


def get_document(db: Session, document_id: int) -> models.Document:
    """Get a document.

    Args:
        db (Session): The session linking to the database
        document_id (int): The document id

    Returns:
        models.Document: The requested document
    """

    return db.query(models.Document).filter(models.Document.id == document_id).first()


def get_documents(
    db: Session, skip: int = 0, limit: int = 100
) -> ty.List[models.Document]:
    """Get documents.

    Args:
        db (Session): The session linking to the database
        skip (int, optional): The number of documents to skip. Defaults to 0.
        limit (int, optional): The number of documents to limit. Defaults to 100.

    Returns:
        ty.List[models.Document]: The requested documents
    """

    return db.query(models.Document).offset(skip).limit(limit).all()
