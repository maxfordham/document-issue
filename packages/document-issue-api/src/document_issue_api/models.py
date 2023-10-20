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
from sqlalchemy.ext.declarative import declarative_base  # TODO: from sqlalchemy.orm import declarative_base


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

    project_role = relationship("ProjectRole", back_populates="person")
    UniqueConstraint(initials)


class Role(Base):
    """Stores the role of a person on a project."""

    # __versioned__ = {}
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String)
    role_description = Column(String)
    is_archived = Column(Boolean, default=False)  # use if a role is no longer required but already in use historically.

    document_role = relationship("DocumentRole", back_populates="role")
    project_role = relationship("ProjectRole", back_populates="role")
    UniqueConstraint(role_name)


class ProjectRole(Base):
    __tablename__ = "project_role"
    project_id = Column(Integer, ForeignKey("project.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("role.id"), primary_key=True)
    person_id = Column(Integer, ForeignKey("person.id"))

    role = relationship("Role", back_populates="project_role")
    project = relationship("Project", back_populates="project_role")
    person = relationship("Person", back_populates="project_role")

    UniqueConstraint(project_id, role_id)


class Project(Base):
    """Stores the project/job number."""

    # __versioned__ = {}
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, index=True)
    project_number = Column(Integer)
    project_name = Column(String)  #  remove / get from webapp

    project_role = relationship("ProjectRole", back_populates="project", cascade="all, delete-orphan")
    document = relationship("Document", back_populates="project", cascade="all, delete-orphan")
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

    document_id = Column(Integer, ForeignKey("document.id"))
    document = relationship("Document", back_populates="issue")


class DocumentRole(Base):
    __tablename__ = "document_role"

    document_id = Column(Integer, ForeignKey("document.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("role.id"), primary_key=True)  # TODO: map to project role

    role = relationship("Role", back_populates="document_role")
    document = relationship("Document", back_populates="document_role")
    UniqueConstraint(document_id, role_id)


class Document(Base):
    """Stores the document number."""

    # __versioned__ = {}
    __tablename__ = "document"

    id = Column(Integer, primary_key=True, index=True)
    name_nomenclature = Column(String)
    document_code = Column(Integer)
    document_description = Column(String)
    document_source = Column(String)
    size = Column(String)
    scale = Column(String)
    notes = Column(JSON)
    originator = Column(String)
    date_string_format = Column(String)
    output_author = Column(Boolean)
    output_checked_by = Column(Boolean)

    # is_archived = Column(Boolean, default=False) # TODO: add for document issued but no longer required

    document_role = relationship("DocumentRole", back_populates="document")

    issue = relationship(
        "Issue",
        back_populates="document",
        cascade="all, delete, delete-orphan",
    )

    project_id = Column(Integer, ForeignKey("project.id"))
    project = relationship("Project", back_populates="document")
    UniqueConstraint(project_id, document_code)  # i.e. unique within project


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

    document_code_generator_id = Column(Integer, ForeignKey("document_code_generator.id"))
