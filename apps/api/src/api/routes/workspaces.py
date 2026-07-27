from fastapi import APIRouter, Depends, HTTPException, status
from src.api.deps import CurrentUserDep, DatabaseDep
from src.db.repositories import WorkspaceMemberRepository, WorkspaceRepository
from src.services.workspace import WorkspaceService
from pymongo import MongoClient

router = APIRouter(prefix="/workspaces", tags=["workspaces"])


def get_workspace_service(db: DatabaseDep):
    from src.settings import settings

    client = MongoClient(settings.mongodb_url, tz_aware=True)
    workspace_repo = WorkspaceRepository(db)
    member_repo = WorkspaceMemberRepository(db)
    return WorkspaceService(workspace_repo, member_repo, client)


# Define the service dependency properly
WorkspaceServiceDep = Depends(get_workspace_service)


@router.post("/", response_model=dict)
def create_workspace(
    data: dict,
    current_user: CurrentUserDep,
    service: WorkspaceService = WorkspaceServiceDep,
):
    name = data.get("name")
    if not name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name is required")

    workspace = service.create_workspace(name=name, owner_id=str(current_user["_id"]))
    return {"id": workspace.id, "name": workspace.name, "slug": workspace.slug}


@router.get("/", response_model=list[dict])
def list_workspaces(current_user: CurrentUserDep, db: DatabaseDep):
    member_repo = WorkspaceMemberRepository(db)
    members = member_repo.list_by_user(str(current_user["_id"]))

    result = []
    for m in members:
        workspace = db["workspaces"].find_one({"_id": m["workspace_id"]})
        if workspace:
            result.append({
                "id": str(workspace["_id"]),
                "name": workspace["name"],
                "slug": workspace["slug"],
                "role": m["role"],
            })

    return result


@router.get("/{workspace_id}/members", response_model=list[dict])
def list_workspace_members(
    workspace_id: str,
    current_user: CurrentUserDep,
    service: WorkspaceService = WorkspaceServiceDep,
):
    members = service.get_workspace_members(workspace_id)
    return [
        {
            "user_id": m.user_id,
            "user_name": m.user_name,
            "role": m.role.value,
            "joined_at": m.joined_at.isoformat(),
        }
        for m in members
    ]