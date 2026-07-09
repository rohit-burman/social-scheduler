# REST API Specification (MVP)

Base URL: `/api/v1`

Authentication:

- Access token: bearer JWT
- Refresh token: httpOnly cookie or secure storage policy

## Auth

### POST /auth/signup

Request:

```json
{
  "email": "user@example.com",
  "password": "StrongPassword123",
  "displayName": "Rohit"
}
```

Response: `201 Created`

### POST /auth/login

Response includes access token and refresh token material.

### POST /auth/refresh

Rotate refresh token and return new pair.

### POST /auth/logout

Revoke current refresh token family session.

## Workspaces

### POST /workspaces

Create workspace. Creator becomes owner.

### GET /workspaces

List user workspaces.

### POST /workspaces/{workspaceId}/invites

Owner can invite members.

### PATCH /workspaces/{workspaceId}/members/{memberId}

Owner can change role.

## Provider Connections

### POST /workspaces/{workspaceId}/providers/mock/connect

Create a mock provider connection.

### DELETE /workspaces/{workspaceId}/providers/{connectionId}

Disconnect provider.

## Posts

### POST /workspaces/{workspaceId}/posts

Create draft post.

### GET /workspaces/{workspaceId}/posts

Filters:

- `status`
- `from`
- `to`
- `provider`

### PATCH /workspaces/{workspaceId}/posts/{postId}

Edit draft (or role/state-allowed transitions).

### POST /workspaces/{workspaceId}/posts/{postId}/schedule

Request:

```json
{
  "scheduledAt": "2026-07-10T15:30:00",
  "timezone": "Asia/Kolkata"
}
```

Response:

```json
{
  "postId": "...",
  "jobId": "...",
  "status": "scheduled"
}
```

### POST /workspaces/{workspaceId}/posts/{postId}/retry

Manual retry for failed post.

## Media

### POST /workspaces/{workspaceId}/media/presign

Return upload URL (R2) or local upload endpoint.

### POST /workspaces/{workspaceId}/media/complete

Commit uploaded media metadata to post.

## Jobs

### GET /workspaces/{workspaceId}/jobs

List jobs with status and next retry info.

### GET /workspaces/{workspaceId}/jobs/{jobId}

Detailed status and attempts.

## Webhooks

### POST /webhooks/providers/mock

Consumes simulated callback payloads.

## Error Response Shape

```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Viewer role cannot schedule posts",
    "requestId": "req_123"
  }
}
```
