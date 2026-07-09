# C4 and Sequence Views

## C4 Context

```mermaid
flowchart TB
  User[Team Member]
  Scheduler[Social Scheduler System]
  Provider[Mock Social Platform]
  ObjStore[Cloudflare R2 / Local Storage]

  User --> Scheduler
  Scheduler --> Provider
  Scheduler --> ObjStore
```

## C4 Container

```mermaid
flowchart LR
  subgraph Scheduler
    Web[Web App Next.js]
    API[API FastAPI]
    Worker[Worker FastAPI Python process]
    DB[(MongoDB)]
    Q[(Redis)]
  end

  Web --> API
  API --> DB
  API --> Q
  API --> Obj[(R2/Local)]
  Worker --> Q
  Worker --> DB
  Worker --> Mock[Mock Provider API]
```

## Sequence: Schedule to Publish

```mermaid
sequenceDiagram
  participant U as User
  participant W as Web
  participant A as API
  participant M as MongoDB
  participant R as Redis
  participant CW as Celery Worker
  participant P as Mock Provider

  U->>W: Schedule post
  W->>A: POST /posts/{id}/schedule
  A->>M: Update post status=scheduled
  A->>R: Enqueue task via Celery
  A-->>W: 202 Accepted
  Note over W: UI status=scheduled
  CW->>R: Consume task from queue
  CW->>P: Publish payload
  alt success
    P-->>CW: 200 ok
    CW->>M: status=published + attempt log
  else failure
    P-->>CW: 500 error
    CW->>R: Requeue with exponential backoff
    CW->>M: status=failed_attempt + log
  end
  W->>A: GET /jobs/{id}
  A-->>W: latest status
```

## Celery Architecture Integration

## Sequence: Refresh Token Rotation

```mermaid
sequenceDiagram
  participant W as Web
  participant A as API
  participant M as MongoDB

  W->>A: POST /auth/refresh (refresh token)
  A->>M: Validate token family + revoke old token
  A->>M: Store new refresh token hash
  A-->>W: New access + refresh token
```

## Failure Handling Model

- Attempt count tracked on each publish job
- Retry delay increases exponentially
- Max attempts transitions job to terminal failed
- Dead-letter list keeps permanent failures for manual action
