import logging
from sqlalchemy.orm import Session
import document_issue_api.document.schemas as schemas
import document_issue_api.models as models
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

    db_document = models.Document(**document.model_dump())
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


def get_document_issue(db: Session, document_id: int) -> schemas.DocumentIssueGet:
    db_ = get_document(db=db, document_id=document_id)
    roles = schemas.ProjectRoles.model_validate(
        [_.role.project_role[0] for _ in db_.document_role]
    )
    d_i = schemas.DocumentIssueGet.model_validate(db_)
    d_i.document_role = roles
    return d_i


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


def patch_document(
    db: Session, document_id: int, document: schemas.DocumentBase
) -> models.Document:
    """Patch a document.

    Args:
        db (Session): The session linking to the database
        document_id (int): The document id
        document (schemas.DocumentBase): The document to patch

    Returns:
        models.Document: The patched document
    """

    db_document = (
        db.query(models.Document).filter(models.Document.id == document_id).first()
    )
    update_data = document.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_document, key, value)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


def delete_document(db: Session, document_id: int) -> models.Document:
    """Delete a document.

    Args:
        db (Session): The session linking to the database
        document_id (int): The document id

    Returns:
        models.Document: The deleted document
    """

    db_document = (
        db.query(models.Document).filter(models.Document.id == document_id).first()
    )
    db.delete(db_document)
    db.commit()
    return db_document
