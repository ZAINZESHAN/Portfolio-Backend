from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.models.admin import Admin


def get_admin_by_email(db: Session, email: str) -> Admin | None:
    return db.query(Admin).filter(Admin.email == email).first()


def authenticate_admin(db: Session, email: str, password: str) -> Admin | None:
    admin = get_admin_by_email(db, email)
    if admin is None or not verify_password(password, admin.hashed_password):
        return None
    return admin
