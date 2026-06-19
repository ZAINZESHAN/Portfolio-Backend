from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import DATABASE_URL
from app.database.base import Base

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")

_connect_args: dict[str, str] = {}
if "localhost" not in DATABASE_URL and "127.0.0.1" not in DATABASE_URL:
    _connect_args["sslmode"] = "require"

engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,
    pool_pre_ping=True,
    connect_args=_connect_args,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    import app.models  # noqa: F401

    Base.metadata.create_all(bind=engine)
