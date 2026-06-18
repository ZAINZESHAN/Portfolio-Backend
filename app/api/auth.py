from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin
from app.core.security import create_access_token
from app.database.db import get_db
from app.models.admin import Admin
from app.schemas.admin import AdminLogin, AdminResponse, Token
from app.services.admin_service import authenticate_admin

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(credentials: AdminLogin, db: Annotated[Session, Depends(get_db)]):
    admin = authenticate_admin(db, credentials.email, credentials.password)
    if admin is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": admin.email})
    return Token(access_token=access_token)


@router.get("/me", response_model=AdminResponse)
def get_me(current_admin: Annotated[Admin, Depends(get_current_admin)]):
    return current_admin
