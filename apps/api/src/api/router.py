from fastapi import APIRouter
from src.api.routes.auth import router as auth_router
from src.api.routes.users import router as users_router
from src.api.routes.workspaces import router as workspaces_router
from src.api.routes.posts import router as posts_router


api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(workspaces_router)
api_router.include_router(posts_router)
