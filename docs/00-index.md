# Social Scheduler Documentation Index

This documentation is designed so you can complete the project end-to-end on your own.

## How to Use This Documentation

Follow this exact order:

1. Product and architecture
2. Data and API contracts
3. Backend implementation
4. Frontend implementation
5. Testing
6. DevOps and deployment
7. Runbooks and recovery

## Reading Order (Required)

1. `product/01-mvp-scope.md`
2. `architecture/01-system-overview.md`
3. `architecture/02-c4-and-sequence.md`
4. `data/01-mongodb-schema.md`
5. `data/02-redis-queues-and-retry.md`
6. `api/01-rest-api-spec.md`
7. `security/01-security-and-rbac.md`
8. `backend/01-backend-implementation-guide.md`
9. `frontend/01-frontend-implementation-guide.md`
10. `testing/01-testing-strategy.md`
11. `devops/01-local-dev-and-env.md`
12. `devops/02-ci-cd-and-release.md`
13. `devops/03-deployment-topology.md`
14. `runbooks/01-operations-runbook.md`
15. `runbooks/02-disaster-recovery.md`

## Definition of Done

Project is complete when all are true:

- MVP checklist from product doc is fully implemented
- API and worker run as separate processes
- MongoDB + Redis data flow is verified with tests
- Retry and failure states are visible in UI
- CI passes on every PR
- Deployment has rollback and backup procedures
- Runbooks are tested at least once

## Technical Scope Summary

- Monorepo: pnpm + turbo + Python services
- Frontend: Next.js App Router + TypeScript
- Backend: FastAPI API + worker process
- Data: MongoDB + Redis
- Storage: local or Cloudflare R2
- Auth: email/password with JWT access + refresh rotation
- Realtime: polling first, websocket optional enhancement

## Suggested Build Milestones

1. Foundation: auth + workspace + RBAC
2. Composition: posts + media upload
3. Scheduling: queue jobs + status model
4. Publishing: mock provider + retries + audit log
5. Visibility: dashboard + status updates
6. Hardening: tests + observability + security
7. Shipping: CI/CD + production deployment
