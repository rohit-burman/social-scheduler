# Social Scheduler Monorepo

Production-style monorepo for a **Social Content Automation Scheduler** built with:

- Next.js (web app)
- FastAPI (main API)
- Celery (background job queue with scheduler)
- MongoDB (primary data)
- Redis (message broker, result backend, cache)
- Cloudflare R2 (media object storage - optional for development)

This repository is documentation-first so you can build and operate the project independently.

## Monorepo Layout

```text
apps/
  web/        # Next.js UI (App Router + TypeScript)
  api/        # FastAPI HTTP API + Celery integration
  worker/     # Placeholder (Celery workers run from API via CLI commands)
packages/
  types/      # Shared TypeScript types and contracts
  config/     # Shared lint/format/tsconfig presets
infra/
  docker/     # Dockerfiles and compose fragments
  kubernetes/ # K8s manifests (starter)
  terraform/  # IaC (Cloudflare R2 starter)
docs/
  architecture/
  product/
  backend/
  frontend/
  data/
  api/
  devops/
  security/
  testing/
  runbooks/
```

## Quick Start

1. Read docs in order:
   - `docs/product/00-project-overview.md` - Project summary
   - `docs/architecture/01-system-overview.md` - Architecture
   - `docs/product/01-mvp-scope.md` - Full feature set and scope
   - `docs/backend/03-queue-systems-celery-rq.md` - Celery implementation details
2. Copy environment template:
   - `cp .env.example .env`
3. Install dependencies:
   - `make deps`
4. Start local services:
   - `make up`
5. Run services (in separate terminals):
   - Terminal 1: `make web`
   - Terminal 2: `make api`
   - Terminal 3: `make worker` (Celery worker)
   - Terminal 4: `make scheduler` (Celery Beat scheduler)
4. Start services (separate terminals):
   - Web: `pnpm --filter web dev`
   - API: `cd apps/api && uv run uvicorn src.main:app --reload --port 8000`
   - Worker: `cd apps/worker && uv run python -m src.worker`

## Core Project Guarantees

- API and worker are separate processes
- Jobs are durable in Redis
- Publish attempts are audited in MongoDB
- Workspace RBAC enforced on all workspace-scoped APIs
- Media storage abstraction supports local or R2
- Retry with exponential backoff for failed publish jobs

## Documentation Map

Everything needed to build and run the full project is in `docs/`.

Start with `docs/00-index.md`.
