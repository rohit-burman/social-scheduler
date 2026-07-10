from pydantic import BaseModel,EmailStr,Field
from datetime  import datetime

class UserCreate(BaseModel):
    email:EmailStr
    password :str =Field(min_length=8)
    name:str

class UserResponse(BaseModel):
    id:str
    name:str
    email:EmailStr
    is_active:bool
    created_at:datetime

