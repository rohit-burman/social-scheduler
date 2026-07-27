from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class ProviderType(str, Enum):
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    INSTAGRAM = "instagram"


class ProviderStatus(str, Enum):
    CONNECTED = "connected"
    ERROR = "error"
    DISCONNECTED = "disconnected"


class ProviderConnectionCreate(BaseModel):
    provider_type: ProviderType
    account_name: str


class ProviderConnectionResponse(BaseModel):
    id: str
    workspace_id: str
    provider_type: ProviderType
    account_name: str
    status: ProviderStatus
    created_at: datetime