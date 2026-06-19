import os

from dotenv import load_dotenv

load_dotenv()


def _normalize_database_url(url: str | None) -> str | None:
    if not url:
        return None
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url


DATABASE_URL = _normalize_database_url(os.getenv("DATABASE_URL"))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 60
