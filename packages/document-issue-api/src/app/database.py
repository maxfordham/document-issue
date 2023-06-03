from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import as_declarative, declarative_base
from sqlalchemy.orm import sessionmaker, configure_mappers
import logging
from app.env import ApiEnv

logger = logging.getLogger(__name__)

ENV = ApiEnv()

# AECTEMPLATER_DATABASE_URL = "postgresql://user:password@postgresserver/db"
engine = create_engine(
    ENV.DOCUMENTISSUE_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
