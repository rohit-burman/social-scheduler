from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class PostStatus(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    FAILED = "failed"


class ProviderType(str, Enum):
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    INSTAGRAM = "instagram"


class MediaAsset(BaseModel):
    key: str
    url: str
    mime_type: str
    size: int


class PostCreate(BaseModel):
    content: str = Field(min_length=1, max_length=5000)
    provider_type: ProviderType
    media: list[MediaAsset] = []


class PostUpdate(BaseModel):
    content: str | None = Field(default=None, min_length=1, max_length=5000)
    media: list[MediaAsset] | None = None


class PostResponse(BaseModel):
    id: str
    workspace_id: str
    created_by: str
    provider_type: ProviderType
    content: str
    media: list[dict[str, Any]]
    status: PostStatus
    scheduled_at: datetime | None = None
    timezone: str | None = None
    last_error: str | None = None
    created_at: datetime
    updated_at: datetime


class ScheduleRequest(BaseModel):
    scheduled_at: datetime
    timezone: str = "UTC"