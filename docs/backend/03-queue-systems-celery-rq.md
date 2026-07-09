# Celery Setup and Configuration Guide

## Overview

This project uses **Celery** as the distributed task queue for background job processing. Celery provides:

- Task queueing and processing
- Automatic retry with exponential backoff
- Task routing and priority queues
- Periodic task scheduling (Celery Beat)
- Built-in monitoring dashboard (Flower)
- Horizontal scaling (run multiple workers)
- Result backend storage
- Dead-letter queue handling

Celery integrates with FastAPI and Redis to provide production-grade async job processing for publishing scheduled social media posts.
- Multiple worker types
- Priority queues

## Celery Setup with FastAPI

### 1. Dependencies

Add to `pyproject.toml`:

```toml
[project.optional-dependencies]
celery = [
  "celery>=5.3.0",
  "flower>=2.0.0",
  "kombu>=5.3.0"
]
```

### 2. Configuration

```python
# apps/api/src/config/celery.py
from celery import Celery
from kombu import Exchange, Queue
import os

celery_app = Celery(
    "social-scheduler",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
)

# Configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes hard limit
    task_soft_time_limit=25 * 60,  # 25 minutes soft limit
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    
    # Task routing by type
    task_routes={
        "tasks.publish_to_provider": {"queue": "publish"},
        "tasks.send_notification": {"queue": "notifications"},
    },
    
    # Queue definitions
    task_queues=(
        Queue("default", Exchange("default"), routing_key="default"),
        Queue("publish", Exchange("publish"), routing_key="publish"),
        Queue("notifications", Exchange("notifications"), routing_key="notifications"),
    ),
)

# Task auto-discovery
celery_app.autodiscover_tasks(["src.tasks"])
```

### 3. Task Definition

```python
# apps/api/src/tasks/publish.py
from src.config.celery import celery_app
from datetime import datetime
import httpx
import logging

logger = logging.getLogger(__name__)

@celery_app.task(
    bind=True,
    max_retries=5,
    default_retry_delay=30,  # 30 seconds base
)
def publish_to_provider(self, job_id: str, post_id: str, workspace_id: str):
    """
    Publish post to provider with retry.
    
    Celery handles retry logic automatically with exponential backoff.
    """
    try:
        # Load post from MongoDB
        post = get_post(post_id, workspace_id)
        provider = get_provider_connection(post.provider_connection_id)
        
        # Call provider API
        response = call_provider_api(provider, post)
        
        # Update status
        update_post_status(post_id, workspace_id, "published", response)
        log_attempt(job_id, post_id, True, response.status_code, None)
        
        return {"status": "success", "post_id": post_id}
        
    except Exception as exc:
        # Log attempt
        log_attempt(job_id, post_id, False, None, str(exc))
        
        # Retry with exponential backoff
        # Celery formula: base_delay * (2 ** (retries - 1))
        retry_count = self.request.retries
        countdown = 30 * (2 ** retry_count)
        
        raise self.retry(exc=exc, countdown=countdown)
```

### 4. Running Celery

```bash
# Start worker
celery -A src.config.celery worker --loglevel=info -Q default,publish

# Start scheduler (for periodic tasks)
celery -A src.config.celery beat --loglevel=info

# Monitor with Flower
celery -A src.config.celery events
# Then open http://localhost:5555 in browser
```

---

## Monitoring

### Celery Monitoring
```bash
# Flower web UI (recommended)
celery -A src.config.celery flower

# CLI monitoring
celery -A src.config.celery inspect active
celery -A src.config.celery inspect stats
celery -A src.config.celery events
```

---

## Error Handling and Retries

### Celery Automatic Retry
```python
@celery_app.task(bind=True, max_retries=5)
def publish_to_provider(self, job_id, post_id, workspace_id):
    try:
        # Task logic
        pass
    except Exception as exc:
        # Celery auto-calculates retry delay with exponential backoff
        raise self.retry(exc=exc, countdown=30)
```

---

## Dead Letter Queue

### Celery
```python
@celery_app.task(bind=True, max_retries=5)
def publish_to_provider(self, job_id, post_id, workspace_id):
    try:
        # Task logic
        pass
    except self.MaxRetriesExceededError:
        # Move to dead letter
        log_dead_letter(job_id, post_id, workspace_id, "max retries exceeded")
        update_post_status(post_id, workspace_id, "failed")
```

---

## Database Status Updates

Both queue systems need to update MongoDB with job status:

```python
# Job status transitions
def log_attempt(job_id, post_id, success, response_code, error):
    attempt = {
        "jobId": job_id,
        "postId": post_id,
        "attempt": get_current_attempt_count(job_id),
        "success": success,
        "providerResponse": response_code,
        "errorMessage": error,
        "timestamp": datetime.utcnow()
    }
    db.publish_attempts.insert_one(attempt)

def update_post_status(post_id, workspace_id, status, response=None):
    db.posts.update_one(
        {"_id": ObjectId(post_id), "workspaceId": workspace_id},
        {
            "$set": {
                "status": status,
                "publishedAt": datetime.utcnow() if status == "published" else None,
                "lastError": response.get("error") if response else None,
                "updatedAt": datetime.utcnow()
            }
        }
    )
```

---

## Getting Started with Celery

1. **Install dependencies**: `uv sync` (Celery is included by default)

2. **Create Celery configuration** at `apps/api/src/config/celery.py`

3. **Define your first task** in `apps/api/src/tasks/publish.py`

4. **Start services**:
   ```bash
   # Terminal 1: API
   make api
   
   # Terminal 2: Celery Worker
   make worker
   
   # Terminal 3: Celery Scheduler (optional)
   make scheduler
   
   # Terminal 4: Flower Monitoring (optional)
   make monitor
   ```

5. **Test task enqueueing** from your FastAPI routes

## Next Steps

- Set up task retries with exponential backoff
- Configure task routing by provider type
- Implement dead-letter queue handling
- Setup monitoring and alerting with Flower
- Scale to multiple worker processes
