"""Create an admin user manually (no signup API)."""

import argparse
import getpass
import sys

from app.core.security import hash_password
from app.database.db import SessionLocal, init_db
from app.models.admin import Admin
from app.services.admin_service import get_admin_by_email


def create_admin(username: str, email: str, password: str) -> None:
    init_db()
    db = SessionLocal()

    try:
        if get_admin_by_email(db, email):
            print(f"Admin with email '{email}' already exists.")
            sys.exit(1)

        admin = Admin(
            username=username,
            email=email,
            hashed_password=hash_password(password),
        )
        db.add(admin)
        db.commit()
        print(f"Admin '{username}' created successfully.")
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a portfolio admin user")
    parser.add_argument("--username", required=True, help="Admin username")
    parser.add_argument("--email", required=True, help="Admin email")
    parser.add_argument(
        "--password",
        help="Admin password (prompted securely if omitted)",
    )
    args = parser.parse_args()

    password = args.password or getpass.getpass("Password: ")
    if not password:
        print("Password cannot be empty.")
        sys.exit(1)

    create_admin(args.username, args.email, password)


if __name__ == "__main__":
    main()
