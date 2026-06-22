from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import DATABASE_URL
from app.database.base import Base

_engine: Engine | None = None
SessionLocal: sessionmaker | None = None


def _build_connect_args(url: str) -> dict[str, str]:
    if "localhost" in url or "127.0.0.1" in url:
        return {}
    if "sslmode=" in url:
        return {}
    return {"sslmode": "require"}


def get_engine() -> Engine:
    global _engine

    if _engine is None:
        if not DATABASE_URL:
            raise RuntimeError("DATABASE_URL environment variable is not set")

        _engine = create_engine(
            DATABASE_URL,
            poolclass=NullPool,
            pool_pre_ping=True,
            connect_args=_build_connect_args(DATABASE_URL),
        )

    return _engine


def get_session_local() -> sessionmaker:
    global SessionLocal

    if SessionLocal is None:
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=get_engine(),
        )

    return SessionLocal


def get_db() -> Generator[Session, None, None]:
    db = get_session_local()()
    try:
        yield db
    finally:
        db.close()


def check_db_connection() -> tuple[bool, str]:
    if not DATABASE_URL:
        return False, "DATABASE_URL is not set in environment variables"

    if "localhost" in DATABASE_URL or "127.0.0.1" in DATABASE_URL:
        return False, "DATABASE_URL points to localhost — use a cloud PostgreSQL URL on Vercel"

    try:
        with get_engine().connect() as connection:
            connection.execute(text("SELECT 1"))
        return True, "Connected"
    except Exception as exc:
        return False, str(exc)


def init_db() -> None:
    import app.models  # noqa: F401

    Base.metadata.create_all(bind=get_engine())
