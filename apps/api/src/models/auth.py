from pydantic import BaseModel,EmailStr,Field
from datetime  import datetime

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenPairResponse(BaseModel):
    access_token:str
    refresh_token:str
    token_type:str="bearer"

class RefreshRequest(BaseModel):
    refresh_token:str
