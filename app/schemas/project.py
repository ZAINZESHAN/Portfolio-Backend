from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProjectBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    short_description: str = Field(min_length=1, max_length=500)
    full_description: str = Field(min_length=1)
    tech_stack: str = Field(min_length=1, max_length=500)
    github_url: str = Field(min_length=1, max_length=500)
    live_url: str = Field(min_length=1, max_length=500)
    image_url: str = Field(min_length=1, max_length=500)
    is_featured: bool = False


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    short_description: str | None = Field(default=None, min_length=1, max_length=500)
    full_description: str | None = Field(default=None, min_length=1)
    tech_stack: str | None = Field(default=None, min_length=1, max_length=500)
    github_url: str | None = Field(default=None, min_length=1, max_length=500)
    live_url: str | None = Field(default=None, min_length=1, max_length=500)
    image_url: str | None = Field(default=None, min_length=1, max_length=500)
    is_featured: bool | None = None


class ProjectResponse(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
