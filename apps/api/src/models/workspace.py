from datetime import datetime

from pydantic import BaseModel, Field


class WorkspaceCreate(BaseModel):
    name:str=Field(
        min_length=3,
        max_length=100
    )

class WorkspaceResponse(BaseModel):
    id:str
    name:str
    slug:str
    created_at:datetime

