from pydantic import BaseModel,EmailStr,Field
from datetime  import datetime


class AccessTokenResponse(BaseModel):
    access_token:str
    token_type:str
