from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class WorkspaceMemberRole(str, Enum):
    OWNER = "owner"
    EDITOR = "editor"
    VIEWER = "viewer"


class WorkspaceCreate(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=100
    )


class WorkspaceResponse(BaseModel):
    id: str
    name: str
    slug: str
    created_at: datetime


class WorkspaceMemberResponse(BaseModel):
    user_id: str
    user_name: str
    role: WorkspaceMemberRole
    joined_at: datetime


class InviteMemberRequest(BaseModel):
    email: str


class UpdateMemberRoleRequest(BaseModel):
    role: WorkspaceMemberRole


class RemoveMemberRequest(BaseModel):
    user_id: str