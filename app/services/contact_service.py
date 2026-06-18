from sqlalchemy.orm import Session

from app.models.contact import Contact
from app.schemas.contact import ContactCreate


def create_contact(db: Session, contact_data: ContactCreate) -> Contact:
    contact = Contact(**contact_data.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def get_all_contacts(db: Session) -> list[Contact]:
    return db.query(Contact).order_by(Contact.created_at.desc()).all()


def get_contact_by_id(db: Session, contact_id: int) -> Contact | None:
    return db.query(Contact).filter(Contact.id == contact_id).first()


def mark_as_read(db: Session, contact_id: int) -> Contact | None:
    contact = get_contact_by_id(db, contact_id)
    if contact is None:
        return None

    contact.is_read = True
    db.commit()
    db.refresh(contact)
    return contact


def delete_contact(db: Session, contact_id: int) -> bool:
    contact = get_contact_by_id(db, contact_id)
    if contact is None:
        return False

    db.delete(contact)
    db.commit()
    return True
