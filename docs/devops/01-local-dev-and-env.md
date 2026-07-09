# Local Development and Environment Setup

## Prerequisites

- Node.js 22+
- pnpm 9+
- Python 3.12+
- uv
- Docker + Docker Compose

## First-Time Setup

1. `cp .env.example .env`
2. Install dependencies:
   - `make deps` (installs with Celery)
3. `make up`

## Run Services

In separate terminals:

```bash
# Terminal 1: Web (Next.js dev server)
make web

# Terminal 2: API (FastAPI)
make api

# Terminal 3: Celery Worker (processes tasks)
make worker

# Terminal 4: Celery Scheduler (schedules periodic tasks)
make scheduler

# Optional Terminal: Celery Flower Monitoring
make monitor
```

All services will log to their respective terminals.

## Local URLs

- Web: `http://localhost:3000`
- API: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- Flower (Celery monitoring): `http://localhost:5555`
- MongoDB: `mongodb://localhost:27017`
- Redis: `redis://localhost:6379`

## Environment Variables

Global:

- `APP_ENV`
- `JWT_SECRET`
- `JWT_REFRESH_SECRET`

API:

- `MONGODB_URL`
- `REDIS_URL`
- `MEDIA_STORAGE_DRIVER`

Celery Configuration:

- `CELERY_BROKER_URL` (defaults to REDIS_URL)
- `CELERY_RESULT_BACKEND` (defaults to REDIS_URL)
- `CELERY_TASK_SERIALIZER` (default: json)
- `CELERY_RESULT_SERIALIZER` (default: json)

Storage:

- R2 credentials when using cloud storage

## Local Verification Checklist

- API `/health` returns OK
- Worker starts and idles without crash
- Mongo and Redis reachable from API
- Draft creation works from web to API
