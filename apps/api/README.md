# API Service

FastAPI service for auth, workspace, post composition, schedule management, and job visibility.

## Run

```bash
uv sync
uv run uvicorn src.main:app --reload --port 8000
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login with email and password
- `POST /api/v1/auth/refresh` - Refresh access token

### Workspaces
- `POST /api/v1/workspaces` - Create a new workspace
- `GET /api/v1/workspaces` - List user's workspaces
- `GET /api/v1/workspaces/{workspace_id}/members` - List workspace members

### Posts
- `POST /api/v1/posts` - Create a draft post
- `GET /api/v1/posts` - List posts (with filters)
- `GET /api/v1/posts/{post_id}` - Get a specific post
- `PATCH /api/v1/posts/{post_id}` - Update a draft post
- `POST /api/v1/posts/{post_id}/schedule` - Schedule a post

### Status Codes
- `200 OK` - Request successful
- `201 Created` - Resource created
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Missing or invalid token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `409 Conflict` - Invalid state transition

## Data Models

### Post Status
- `draft` - Post is being composed
- `scheduled` - Post is scheduled for future publishing
- `published` - Post was successfully published
- `failed` - Post failed after max retries

### Roles
- `owner` - Full control
- `editor` - Can create and schedule posts
- `viewer` - Read-only access