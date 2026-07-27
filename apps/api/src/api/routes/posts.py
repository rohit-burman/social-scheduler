from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from datetime import UTC, datetime, timedelta

from src.api.deps import CurrentUserDep, DatabaseDep, RedisDep
from src.db.repositories import WorkspaceMemberRepository
from src.models.post import (
    PostCreate,
    PostResponse,
    PostStatus,
    ProviderType,
    ScheduleRequest,
    MediaAsset,
)

router = APIRouter(prefix="/posts", tags=["posts"])


def get_media_upload_url(key: str) -> str:
    """In production, this would return a presigned URL. For MVP, just simulate."""
    return f"/media/{key}"


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_post(
    data: PostCreate,
    current_user: CurrentUserDep,
    db: DatabaseDep,
):
    workspace_member_repo = WorkspaceMemberRepository(db)
    member = workspace_member_repo.get_membership_by_user(str(current_user["_id"]))

    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of any workspace",
        )

    post_doc = {
        "workspace_id": member["workspace_id"],
        "created_by": ObjectId(current_user["_id"]),
        "provider_type": data.provider_type.value,
        "content": data.content,
        "media": [m.model_dump() for m in data.media] if data.media else [],
        "status": PostStatus.DRAFT.value,
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
    }

    result = db["posts"].insert_one(post_doc)
    post_doc["_id"] = result.inserted_id

    return {
        "id": str(post_doc["_id"]),
        "workspace_id": str(post_doc["workspace_id"]),
        "provider_type": post_doc["provider_type"],
        "content": post_doc["content"],
        "media": post_doc["media"],
        "status": post_doc["status"],
        "scheduled_at": None,
        "timezone": None,
        "last_error": None,
        "created_at": post_doc["created_at"].isoformat(),
        "updated_at": post_doc["updated_at"].isoformat(),
    }


@router.get("/", response_model=list[dict])
def list_posts(
    status_filter: str | None = None,
    provider_type: str | None = None,
    current_user: CurrentUserDep = None,
    db: DatabaseDep = None,
):
    if not current_user or not db:
        return []
        
    workspace_member_repo = WorkspaceMemberRepository(db)
    member = workspace_member_repo.get_membership_by_user(str(current_user["_id"]))

    if not member:
        return []

    query = {"workspace_id": member["workspace_id"]}
    if status_filter:
        query["status"] = status_filter
    if provider_type:
        query["provider_type"] = provider_type

    posts = list(db["posts"].find(query).sort("created_at", -1).limit(50))

    return [
        {
            "id": str(p["_id"]),
            "workspace_id": str(p["workspace_id"]),
            "provider_type": p["provider_type"],
            "content": p["content"],
            "media": p["media"],
            "status": p["status"],
            "scheduled_at": p.get("scheduled_at").isoformat() if p.get("scheduled_at") else None,
            "timezone": p.get("timezone"),
            "last_error": p.get("last_error"),
            "created_at": p["created_at"].isoformat(),
            "updated_at": p["updated_at"].isoformat(),
        }
        for p in posts
    ]


@router.get("/{post_id}", response_model=dict)
def get_post(post_id: str, current_user: CurrentUserDep = None, db: DatabaseDep = None):
    if not current_user or not db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    workspace_member_repo = WorkspaceMemberRepository(db)
    member = workspace_member_repo.get_membership_by_user(str(current_user["_id"]))

    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    post = db["posts"].find_one({"_id": ObjectId(post_id), "workspace_id": member["workspace_id"]})

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    return {
        "id": str(post["_id"]),
        "workspace_id": str(post["workspace_id"]),
        "provider_type": post["provider_type"],
        "content": post["content"],
        "media": post["media"],
        "status": post["status"],
        "scheduled_at": post.get("scheduled_at").isoformat() if post.get("scheduled_at") else None,
        "timezone": post.get("timezone"),
        "last_error": post.get("last_error"),
        "created_at": post["created_at"].isoformat(),
        "updated_at": post["updated_at"].isoformat(),
    }


@router.patch("/{post_id}", response_model=dict)
def update_post(
    post_id: str,
    data: dict,
    current_user: CurrentUserDep = None,
    db: DatabaseDep = None,
):
    if not current_user or not db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    workspace_member_repo = WorkspaceMemberRepository(db)
    member = workspace_member_repo.get_membership_by_user(str(current_user["_id"]))

    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    post = db["posts"].find_one({"_id": ObjectId(post_id), "workspace_id": member["workspace_id"]})

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if post["status"] != PostStatus.DRAFT.value:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot edit post that is not a draft",
        )

    update_data = {"updated_at": datetime.now(UTC)}
    if "content" in data:
        update_data["content"] = data["content"]
    if "media" in data:
        update_data["media"] = data["media"]

    db["posts"].update_one({"_id": ObjectId(post_id)}, {"$set": update_data})

    updated_post = db["posts"].find_one({"_id": ObjectId(post_id)})
    return {
        "id": str(updated_post["_id"]),
        "workspace_id": str(updated_post["workspace_id"]),
        "provider_type": updated_post["provider_type"],
        "content": updated_post["content"],
        "media": updated_post["media"],
        "status": updated_post["status"],
        "scheduled_at": updated_post.get("scheduled_at").isoformat() if updated_post.get("scheduled_at") else None,
        "timezone": updated_post.get("timezone"),
        "last_error": updated_post.get("last_error"),
        "created_at": updated_post["created_at"].isoformat(),
        "updated_at": updated_post["updated_at"].isoformat(),
    }


@router.post("/{post_id}/schedule", response_model=dict)
def schedule_post(
    post_id: str,
    data: ScheduleRequest,
    current_user: CurrentUserDep = None,
    db: DatabaseDep = None,
    redis: RedisDep = None,
):
    if not current_user or not db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    workspace_member_repo = WorkspaceMemberRepository(db)
    member = workspace_member_repo.get_membership_by_user(str(current_user["_id"]))

    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    post = db["posts"].find_one({"_id": ObjectId(post_id), "workspace_id": member["workspace_id"]})

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if post["status"] != PostStatus.DRAFT.value:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only draft posts can be scheduled",
        )

    # Parse timezone offset
    tz_offset = 0
    if data.timezone.upper() != "UTC":
        try:
            if data.timezone.startswith(("+", "-")):
                parts = data.timezone[1:].split(":")
                if len(parts) == 2:
                    tz_offset = int(parts[0])
        except Exception:
            pass

    scheduled_utc = data.scheduled_at - timedelta(hours=tz_offset)

    if scheduled_utc < datetime.now(UTC):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Scheduled time must be in the future")

    job_id = f"job_{post_id}_{int(scheduled_utc.timestamp())}"

    job_doc = {
        "post_id": ObjectId(post_id),
        "job_id": job_id,
        "scheduled_at": scheduled_utc,
        "status": "scheduled",
        "attempt": 0,
        "max_attempts": 5,
        "created_at": datetime.now(UTC),
    }

    db["publish_jobs"].insert_one(job_doc)

    db["posts"].update_one(
        {"_id": ObjectId(post_id)},
        {
            "$set": {
                "status": PostStatus.SCHEDULED.value,
                "scheduled_at": scheduled_utc,
                "timezone": data.timezone,
                "updated_at": datetime.now(UTC),
            }
        },
    )

    post_doc = db["posts"].find_one({"_id": ObjectId(post_id)})

    return {
        "id": str(post_doc["_id"]),
        "workspace_id": str(post_doc["workspace_id"]),
        "provider_type": post_doc["provider_type"],
        "content": post_doc["content"],
        "media": post_doc["media"],
        "status": post_doc["status"],
        "scheduled_at": post_doc["scheduled_at"].isoformat(),
        "timezone": post_doc.get("timezone"),
        "last_error": None,
        "created_at": post_doc["created_at"].isoformat(),
        "updated_at": post_doc["updated_at"].isoformat(),
        "job_id": job_id,
    }