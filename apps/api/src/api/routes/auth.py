from fastapi import APIRouter, HTTPException, status, Depends,Request
from pymongo.errors import DuplicateKeyError
from src.api.deps import AuthServiceDep,LoginRateLimiterDep
from src.exceptions import InvalidRefreshTokenError, RefreshTokenReuseError
from src.models.user import UserResponse, UserCreate
from src.models.auth import TokenPairResponse, LoginRequest, RefreshRequest
from fastapi.security import OAuth2PasswordRequestForm

from src.services.rate_limit import build_login_failure_key

router = APIRouter(prefix="/auth",tags=["auth"])

@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def register(user_data:UserCreate,auth_service:AuthServiceDep)->UserResponse:
    try:
        return await auth_service.register(user_data)
    except DuplicateKeyError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email already registered") from e


@router.post("/login", response_model=TokenPairResponse)
async def login(cred: LoginRequest, auth_service: AuthServiceDep,limiter:LoginRateLimiterDep,request:Request) -> TokenPairResponse:
    client_ip = request.client.host if request.client else "unknown"
    key = build_login_failure_key(client_ip,str(cred.email))

    if await limiter.is_limited(key):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,detail="Too many login attempts. Try again later.")


    user = await auth_service.authenticate(cred)

    if not user:
        await limiter.record_failure(key)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password",
                            headers={"WWW-Authenticate": "Bearer"})

    await limiter.clear(key)
    access_token,refresh_token = (await auth_service.issue_token_pair(user_id=str(user["_id"])))
    return TokenPairResponse(access_token=access_token,refresh_token=refresh_token, token_type="bearer")

@router.post("/refresh",response_model=TokenPairResponse)
async def refresh(request_data:RefreshRequest,auth_service:AuthServiceDep)->TokenPairResponse:
    try:
        access_token,refresh_token =( await auth_service.rotate_refresh_token(request_data.refresh_token))
    except (InvalidRefreshTokenError,RefreshTokenReuseError) as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid refresh token") from e

    return TokenPairResponse(access_token=access_token,refresh_token=refresh_token)

# @router.post("/login", response_model=AccessTokenResponse)
# async def login(form_data: OAuth2PasswordRequestForm = Depends(),auth_service: AuthServiceDep = None):
#     user = await auth_service.authenticate(
#         LoginRequest(
#             email=form_data.username,
#             password=form_data.password
#         )
#     )
#     if not user:
#         raise HTTPException(status_code=401,detail="Invalid email or password")
#
#     access_token = create_access_token(str(user["_id"]))
#
#     return AccessTokenResponse(
#         access_token=access_token,
#         token_type="bearer"
#     )
