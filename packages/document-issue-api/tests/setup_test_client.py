from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.env import ApiEnv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pathlib
from app.models import Base

FPTH_API_TEST_ENV = pathlib.Path(__file__).parent.parent / "api-test.env"
ENV = ApiEnv(_env_file=FPTH_API_TEST_ENV, _env_file_encoding="utf-8")

# --------------- equivalent to: app./database.py ---------------------

engine = create_engine(
    ENV.DOCUMENTISSUE_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def get_db_path():
    return pathlib.Path(ENV.DOCUMENTISSUE_DATABASE_URL.replace("sqlite:///", ""))


def clean_session():
    """Delete old test.db before creating it again"""
    get_db_path().unlink(missing_ok=True)
    Base.metadata.create_all(bind=engine)


clean_session()
engine = create_engine(
    ENV.DOCUMENTISSUE_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)
