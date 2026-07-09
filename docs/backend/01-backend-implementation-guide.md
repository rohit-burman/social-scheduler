# Backend Implementation Guide (FastAPI + Celery)

## Objective

Build a production-style backend with clear boundaries:

- API process handles HTTP and orchestration
- **Celery** distributed task queue handles asynchronous publishing
- Workers consume tasks from Redis message broker
- Celery Beat manages scheduled/periodic tasks

See [docs/backend/03-queue-systems-celery-rq.md](03-queue-systems-celery-rq.md) for detailed Celery setup and configuration.

## Celery Architecture

Celery is a distributed task queue that:
- Runs as separate worker processes
- Consumes tasks from Redis message broker
- Supports automatic retry with exponential backoff
- Provides task routing and priority queues
- Includes Flower web-based monitoring
- Scales horizontally (run multiple workers)
- Manages periodic tasks via Celery Beat scheduler

## Suggested API Folder Structure

```text
apps/api/src/
  main.py
  settings.py
  api/
    routes/
      auth.py
      workspaces.py
      posts.py
      media.py
      jobs.py
      providers.py
  domain/
    auth/
    workspaces/
    posts/
    jobs/
  infra/
    mongodb/
    redis/
    storage/
    providers/
  schemas/
  services/
  dependencies/
```

## Suggested Worker Folder Structure

```text
apps/worker/src/
  worker.py
  settings.py
  queue/
    consumer.py
    scheduler.py
  publish/
    executor.py
    retry.py
  providers/
    mock_provider.py
  repositories/
    jobs_repo.py
    posts_repo.py
```

## Implementation Steps

1. Configure settings and dependency injection
2. Implement auth:
   - Password hashing
   - Access and refresh token pair
   - Refresh token family table/collection for rotation
3. Implement workspace and membership endpoints
4. Add RBAC dependency checks per route
5. Create post CRUD and draft lifecycle
6. Add media upload abstraction:
   - Local driver
   - R2 driver
7. Add schedule endpoint:
   - Validate future datetime in UTC
   - Insert publish job record
   - Enqueue delayed Redis job
8. Implement worker consumer loop
9. Implement provider adapter and failure simulation
10. Add retry and terminal failure handling
11. Add audit logging for each attempt

## Status State Machine

- `draft`
- `scheduled`
- `publishing`
- `published`
- `failed` (terminal)

Rules:

- `draft -> scheduled`
- `scheduled -> publishing`
- `publishing -> published`
- `publishing -> failed` (terminal only after max retries)

## Queue Contract

Job payload example:

```json
{
  "jobId": "job_123",
  "workspaceId": "ws_1",
  "postId": "post_9",
  "provider": "mock_twitter",
  "scheduledAt": "2026-07-10T12:00:00Z",
  "attempt": 1,
  "maxAttempts": 5
}
```

## Idempotency Rules

- Use `jobId` as idempotency key
- Before publishing, check terminal status
- Ignore duplicate queue deliveries after terminal states

## Error Handling

- Validation errors: 400
- Auth errors: 401/403
- Not found: 404
- Conflict for invalid state transitions: 409
- Internal worker or provider errors: logged + retry path

## Performance Tips

- Keep API handlers thin, business logic in services
- Batch status polling endpoint responses
- Use Mongo indexes for workspace + status + scheduledAt queries

## Definition of Done (Backend)

- Full endpoint coverage for MVP
- Worker processes delayed jobs reliably
- Retry and dead-letter flow tested
- OpenAPI docs generated and reviewed
