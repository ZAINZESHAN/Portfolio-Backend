import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import admin, auth, contact, projects
from app.core.config import DATABASE_URL, SECRET_KEY
from app.database.db import check_db_connection, init_db

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not DATABASE_URL:
        logger.warning("DATABASE_URL is missing — API routes that need the database will fail")
    elif not SECRET_KEY:
        logger.warning("SECRET_KEY is missing — authentication will fail")
    else:
        try:
            init_db()
            logger.info("Database initialized successfully")
        except Exception as exc:
            logger.error("Database initialization failed: %s", exc)

    yield


app = FastAPI(
    title="Portfolio API",
    description="Backend API for a personal developer portfolio",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(contact.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"message": "Portfolio API is running"}


@app.get("/health")
def health():
    db_ok, db_message = check_db_connection()
    return {
        "status": "ok" if db_ok else "degraded",
        "database": {
            "connected": db_ok,
            "message": db_message,
        },
        "env": {
            "database_url_set": bool(DATABASE_URL),
            "secret_key_set": bool(SECRET_KEY),
        },
    }
