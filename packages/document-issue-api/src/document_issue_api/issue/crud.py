import logging
from sqlalchemy.orm import Session
import document_issue_api.issue.schemas as schemas
import document_issue_api.models as models
import typing as ty
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)


# issue
def post_issue(db: Session, issue: schemas.IssueBasePost) -> models.Issue:
    """Create a new issue.

    Args:
        db (Session): The session linking to the database
        issue (schemas.IssueBasePost): The issue to post

    Returns:
        models.Issue: The postd issue
    """

    db_issue = models.Issue(**issue.dict())  #
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue
