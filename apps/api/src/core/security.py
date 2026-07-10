from pwdlib import PasswordHash
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import UTC,timedelta,datetime
from uuid import uuid4
from typing import Any
from src.settings import settings
from fastapi.security import OAuth2PasswordBearer

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")  #to let swagger know the endpoint where login happens

def hash_password(password:str)->str:
    return password_hash.hash(password)

def verify_password(plain_password:str,hashed_password:str)->bool:
    return password_hash.verify(plain_password,hashed_password)

def create_access_token(user_id:str)->str:
    now = datetime.now(UTC)
    payload= {
        "sub":user_id,
        "type":"access",
        "iat":now,
        "exp":now+timedelta(minutes=settings.access_token_expire_minutes),
        "jti":str(uuid4())
    }

    return jwt.encode(payload,settings.jwt_secret,algorithm="HS256")

def decode_access_token(access_token:str)->dict:
    return jwt.decode(access_token,settings.jwt_secret,algorithms=["HS256"])


