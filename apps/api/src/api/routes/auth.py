from fastapi import APIRouter, HTTPException, status, Depends
from pymongo.errors import DuplicateKeyError
from src.api.deps import AuthServiceDep
from src.core.secutity import create_access_token
from src.models.user import UserResponse, UserCreate, LoginRequest
from src.models.auth import AccessTokenResponse
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth",tags=["auth"])

@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def register(user_data:UserCreate,auth_service:AuthServiceDep)->UserResponse:
    try:
        return await auth_service.register(user_data)
    except DuplicateKeyError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email already registered") from e

# @router.post("/login",response_model=AccessTokenResponse)
# async def login(cred:LoginRequest,auth_service:AuthServiceDep)->AccessTokenResponse:
 #     user = await auth_service.authenticate(cred)
#
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid email or password",headers={"WWW-Authenticate":"Bearer"})
#
#     access_token = create_access_token(user_id=str(user["_id"]))
#     return AccessTokenResponse(access_token=access_token,token_type="bearer")

@router.post("/login", response_model=AccessTokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),auth_service: AuthServiceDep = None):
    user = await auth_service.authenticate(
        LoginRequest(
            email=form_data.username,
            password=form_data.password
        )
    )
    if not user:
        raise HTTPException(status_code=401,detail="Invalid email or password")

    access_token = create_access_token(str(user["_id"]))

    return AccessTokenResponse(
        access_token=access_token,
        token_type="bearer"
    )
