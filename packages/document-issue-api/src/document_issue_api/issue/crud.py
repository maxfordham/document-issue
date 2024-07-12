import logging
from sqlalchemy.orm import Session
import document_issue_api.issue.schemas as schemas
import document_issue_api.models as models
import typing as ty
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)


# issue
def post_issue(db: Session, document_id: int, issue: schemas.IssueBasePost) -> models.Issue:
    """Create a new issue.

    Args:
        db (Session): The session linking to the database
        issue (schemas.IssueBasePost): The issue to post

    Returns:
        models.Issue: The postd issue
    """

    db_issue = models.Issue(**issue.model_dump(exclude="issue_id") | {"document_id": int(document_id)})  #
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue


def get_issue(db: Session, issue_id: int) -> models.Issue:
    """Get an issue.

    Args:
        db (Session): The session linking to the database
        issue_id (int): The id of the issue to get

    Returns:
        models.Issue: The getd issue
    """

    db_issue = db.query(models.Issue).get(issue_id)
    return db_issue


def patch_issue(db: Session, issue_id: int, issue: schemas.IssueBasePatch) -> models.Issue:
    """Patch an issue.

    Args:
        db (Session): The session linking to the database
        issue_id (int): The id of the issue to patch
        issue (schemas.IssueBasePatch): The issue patch

    Returns:
        models.Issue: The patched issue
    """

    db_issue = db.query(models.Issue).get(issue_id)
    issue_data = jsonable_encoder(db_issue)
    update_data = issue.model_dump(exclude_unset=True)
    for field in issue_data:
        if field in update_data:
            setattr(db_issue, field, update_data[field])
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue


def delete_issue(db: Session, issue_id: int) -> models.Issue:
    """Delete an issue.

    Args:
        db (Session): The session linking to the database
        issue_id (int): The id of the issue to delete

    Returns:
        models.Issue: The deleted issue
    """

    db_issue = db.query(models.Issue).get(issue_id)
    db.delete(db_issue)
    db.commit()
    return db_issue
