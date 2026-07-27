from datetime import UTC, datetime

from bson import ObjectId
from pymongo.asynchronous.client_session import AsyncClientSession
from pymongo.asynchronous.mongo_client import AsyncMongoClient
from pymongo.errors import DuplicateKeyError

from src.core.slug import slugify
from src.db.repositories import WorkspaceMemberRepository,WorkspaceRepository
from src.exceptions import WorkspaceCreationError
from src.models.workspace import WorkspaceResponse

MAX_SLUG_ATTEMPTS = 25


class WorkspaceService:
    def __init__(self,workspace_repository: WorkspaceRepository,workspace_member_repository: WorkspaceMemberRepository,mongo_client: AsyncMongoClient) -> None:
        self.workspace_repository = workspace_repository
        self.workspace_member_repository = workspace_member_repository
        self.mongo_client = mongo_client

    async def create_workspace(self,*,name: str,owner_id: str) -> WorkspaceResponse:
        base_slug = slugify(name)
        now = datetime.now(UTC)

        for attempt in range(MAX_SLUG_ATTEMPTS):
            candidate = generate_slug_candidate(base_slug, attempt)

            workspace_document = {
                "name": name,
                "slug": candidate,
                "created_by": ObjectId(owner_id),
                "created_at": now,
            }

            try:
                async def callback(session: AsyncClientSession) -> str:
                    create_workspace_id = await self.workspace_repository.create(
                        document=workspace_document,
                        session=session,
                    )

                    await self.workspace_member_repository.create(
                        document={
                            "workspace_id": ObjectId(create_workspace_id),
                            "user_id": ObjectId(owner_id),
                            "role": "OWNER",
                            "joined_at": now,
                        },
                        session=session,
                    )

                    return create_workspace_id

                async with self.mongo_client.start_session() as s:
                    workspace_id = await s.with_transaction(callback)


                return WorkspaceResponse(
                    id=str(workspace_id),
                    name=name,
                    slug=candidate,
                    created_at=now,
                )

            except DuplicateKeyError:
                continue

        raise WorkspaceCreationError()


def generate_slug_candidate(base_slug: str, attempt: int) -> str:
    if attempt == 0:
        return base_slug

    return f"{base_slug}-{attempt + 1}"
