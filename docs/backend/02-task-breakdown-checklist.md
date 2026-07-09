# Backend Task Breakdown Checklist

## Auth

- [ ] Signup endpoint and validation
- [ ] Login endpoint and password verification
- [ ] Access token issuance
- [ ] Refresh token rotation and revocation
- [ ] Logout endpoint

## Workspace and RBAC

- [ ] Create workspace
- [ ] Invite member
- [ ] Accept invite flow
- [ ] Role update endpoint
- [ ] RBAC guard wired on all routes

## Posts and Media

- [ ] Draft post CRUD
- [ ] Media validation service
- [ ] Local upload driver
- [ ] R2 upload driver
- [ ] Post attachment finalization

## Scheduling and Jobs

- [ ] Schedule endpoint with timezone conversion
- [ ] Queue enqueue with delayed execution
- [ ] Job status endpoint
- [ ] Retry endpoint for failed posts

## Celery Worker

- [ ] Configure Celery broker (Redis)
- [ ] Configure Celery result backend (Redis)
- [ ] Create Celery app instance with settings
- [ ] Define task decorators (@app.task)
- [ ] Implement publish_to_provider task
- [ ] Configure task routing and queues
- [ ] Implement retry policy with exponential backoff
- [ ] Configure dead-letter queue for failed tasks
- [ ] Implement task idempotency checks
- [ ] Setup Celery Beat scheduler
- [ ] Configure worker startup and shutdown
- [ ] Implement graceful shutdown (wait for in-flight tasks)
- [ ] Setup Flower monitoring dashboard

## Observability

- [ ] Structured logger
- [ ] Request ID middleware
- [ ] Job correlation IDs
- [ ] Metrics endpoint or exporter

## Hardening

- [ ] Rate limit sensitive endpoints
- [ ] Input schema validation
- [ ] Security event audit logs
- [ ] Integration tests for core flows
