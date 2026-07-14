from pwdlib import PasswordHash
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import UTC,timedelta,datetime
from uuid import uuid4
from typing import Any
from src.settings import settings
from fastapi.security import OAuth2PasswordBearer
import hashlib

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

def create_refresh_token(user_id:str,jti:str,family_id:str,issued_at:datetime,expires_at:datetime)->str:
    payload={
        "sub":user_id,
        "type":"refresh",
        "iat":issued_at,
        "exp":expires_at,
        "jti":jti,
        "family_id":family_id
    }
    return  jwt.encode(payload,settings.jwt_secret,algorithm="HS256")

def decode_token(access_token:str)->dict:
    return jwt.decode(access_token,settings.jwt_secret,algorithms=["HS256"])

def hash_token(token:str)->str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()

