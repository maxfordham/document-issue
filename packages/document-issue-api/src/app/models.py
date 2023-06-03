# import sqlalchemy as sa # TODO
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Date,
    Float,
    UniqueConstraint,
    Enum,
    JSON,
)

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import relationship, configure_mappers, validates
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Role(Base):
    """Stores the role of a person on a project."""

    # __versioned__ = {}
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    role = Column(String)
    is_archived = Column(
        Boolean, default=False
    )  # use if a role is no longer required but already in use historically.

    UniqueConstraint(name)


class ProjectRole(Base):
    __tablename__ = "project_role"
    project_id = Column(Integer, ForeignKey("project.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("role.id"), primary_key=True)


class Project(Base):
    """Stores the project/job number."""

    # __versioned__ = {}
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, index=True)
    project_number = Column(Integer)

    UniqueConstraint(project_number)


class Issue(Base):
    """Stores the issue number."""

    # __versioned__ = {}
    __tablename__ = "issue"

    id = Column(Integer, primary_key=True, index=True)
    revision = Column(String)
    date = Column(Date)
    # status = Column(String)  # maps to status code...
    status_code = Column(String)
    status_description = Column(String)
    author = Column(String)  # must be in project
    checked_by = Column(String)
    issue_format = Column(String)
    issue_notes = Column(String)

    project_id = Column(Integer, ForeignKey("project.id"))
    document_id = Column(Integer, ForeignKey("document.id"))


class Document(Base):
    """Stores the document number."""

    # __versioned__ = {}
    __tablename__ = "document"

    id = Column(Integer, primary_key=True, index=True)
    document_code = Column(Integer)
    document_description = Column(String)

    project_id = Column(Integer, ForeignKey("project.id"))
    UniqueConstraint(document_code)
