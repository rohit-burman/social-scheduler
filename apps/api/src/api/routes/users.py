from fastapi import APIRouter
from src.api.deps import CurrentUserDep
from src.models.user import UserResponse

router = APIRouter(prefix="/users",tags=["Users"])

@router.get("/me", response_model=UserResponse)
async def get_me(curr_user :CurrentUserDep)->UserResponse:
    return UserResponse(
        id=(str(curr_user["_id"])),
        name=curr_user["name"],
        email=curr_user["email"],
        is_active=curr_user["is_active"],
        created_at=curr_user["created_at"]
    )



