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


class Person(Base):
    """Stores the person's initials and full name."""

    # TODO: should this just store ID from WebApp?

    # __versioned__ = {}
    __tablename__ = "person"

    id = Column(Integer, primary_key=True, index=True)
    initials = Column(String)
    full_name = Column(String)

    # project_person = relationship("ProjectRole", back_populates="people")
    UniqueConstraint(initials)


class Role(Base):
    """Stores the role of a person on a project."""

    # __versioned__ = {}
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String)
    role_description = Column(String)
    is_archived = Column(
        Boolean, default=False
    )  # use if a role is no longer required but already in use historically.

    project_role = relationship("ProjectRole", back_populates="role")
    UniqueConstraint(role_name)


class ProjectRole(Base):
    __tablename__ = "project_role"
    project_id = Column(Integer, ForeignKey("project.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("role.id"), primary_key=True)

    role = relationship("Role", back_populates="project_role")
    project = relationship("Project", back_populates="project_role")

    UniqueConstraint(project_id, role_id)


class Project(Base):
    """Stores the project/job number."""

    # __versioned__ = {}
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, index=True)
    project_number = Column(Integer)
    project_name = Column(String)  #  remove / get from webapp

    project_role = relationship("ProjectRole", back_populates="project")
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

    # relationship("Document", back_populates="issue")


class DocumentRole(Base):
    __tablename__ = "document_role"

    document_id = Column(Integer, ForeignKey("document.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("role.id"), primary_key=True)
    project_id = Column(Integer, ForeignKey("project.id"), primary_key=True)

    # project = relationship("Project", back_populates="project_role")

    # role = relationship("Role", back_populates="project_role")
    # document_role = relationship("Document", back_populates="role")
    # get people from project_role
    UniqueConstraint(document_id, role_id)


class Document(Base):
    """Stores the document number."""

    # __versioned__ = {}
    __tablename__ = "document"

    id = Column(Integer, primary_key=True, index=True)
    document_code = Column(Integer)
    document_description = Column(String)

    # role = relationship(
    #     "DocumentRole",
    #     back_populates="document_role",
    #     cascade="all, delete, delete-orphan",
    # )
    # issue = relationship(
    #     "Issue",
    #     back_populates="document",
    #     cascade="all, delete, delete-orphan",
    # )

    project_id = Column(Integer, ForeignKey("project.id"))
    UniqueConstraint(document_code)


# ------------------
# below for future stuff


class Classification(Base):
    """Stores the classification of a document."""

    # __versioned__ = {}
    __tablename__ = "classification"

    id = Column(Integer, primary_key=True, index=True)
    classification_description = Column(String)


class InformationType(Base):
    """Stores the information type of a document."""

    # __versioned__ = {}
    __tablename__ = "information_type"

    id = Column(Integer, primary_key=True, index=True)
    information_type_description = Column(String)


class Originator(Base):
    """Stores the originator of a document."""

    # __versioned__ = {}
    __tablename__ = "originator"

    id = Column(Integer, primary_key=True, index=True)
    originator_description = Column(String)


class Level(Base):
    """Stores the level of a document."""

    # __versioned__ = {}
    __tablename__ = "level"

    id = Column(Integer, primary_key=True, index=True)
    level_description = Column(String)


class DocumentCodeGenerator(Base):
    """Stores the code generation of a document. This the practice default."""

    # __versioned__ = {}
    __tablename__ = "document_code_generator"

    id = Column(Integer, primary_key=True, index=True)
    version = Column(Integer)
    issue_date = Column(Date)
    map_classification = Column(JSON)
    map_information_type = Column(JSON)
    map_level = Column(JSON)
    map_originator = Column(JSON)


class ProjectDocumentCodeGenerator(Base):
    """Stores the code generation of a document for a project. This is the project override"""

    # __versioned__ = {}
    __tablename__ = "project_document_code_generator"

    id = Column(Integer, primary_key=True, index=True)
    map_classification = Column(JSON)  # , allow_null=True)
    map_information_type = Column(JSON)  # , allow_null=True)
    map_level = Column(JSON)  # , allow_null=True)
    map_project = Column(JSON)
    map_originator = Column(JSON)

    document_code_generator_id = Column(
        Integer, ForeignKey("document_code_generator.id")
    )
