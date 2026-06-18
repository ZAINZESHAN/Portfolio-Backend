from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin
from app.database.db import get_db
from app.models.admin import Admin
from app.schemas.contact import ContactResponse
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.services.contact_service import (
    delete_contact,
    get_all_contacts,
    mark_as_read,
)
from app.services.project_service import (
    create_project,
    delete_project,
    update_project,
)

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post(
    "/projects",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_admin_project(
    project_data: ProjectCreate,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[Admin, Depends(get_current_admin)],
):
    return create_project(db, project_data)


@router.put("/projects/{project_id}", response_model=ProjectResponse)
def update_admin_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[Admin, Depends(get_current_admin)],
):
    project = update_project(db, project_id, project_data)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    return project


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin_project(
    project_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[Admin, Depends(get_current_admin)],
):
    deleted = delete_project(db, project_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )


@router.get("/contacts", response_model=list[ContactResponse])
def list_contacts(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[Admin, Depends(get_current_admin)],
):
    return get_all_contacts(db)


@router.patch("/contacts/{contact_id}", response_model=ContactResponse)
def mark_contact_as_read(
    contact_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[Admin, Depends(get_current_admin)],
):
    contact = mark_as_read(db, contact_id)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )
    return contact


@router.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin_contact(
    contact_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[Admin, Depends(get_current_admin)],
):
    deleted = delete_contact(db, contact_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )
