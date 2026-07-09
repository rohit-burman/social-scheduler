# Implementation Roadmap (Week-by-Week)

## Week 1: Foundations

- Setup monorepo, local infra, and health checks
- Implement auth signup/login/refresh/logout
- Create workspace and membership models
- Add RBAC middleware/dependency checks

Deliverable:

- Authenticated user can create workspace and invite member

## Week 2: Post Composition

- Implement post draft CRUD
- Implement media upload abstraction (local first)
- Integrate compose form in frontend
- Role-based UI restrictions

Deliverable:

- Editor can create and update drafts with media

## Week 3: Scheduling and Queue

- Build schedule endpoint
- Add Redis delayed queue and worker consumer
- Add publish job and attempts collections
- Implement mock provider random success/failure

Deliverable:

- Scheduled posts get processed asynchronously

## Week 4: Reliability and Visibility

- Add retry with exponential backoff
- Add terminal fail and dead-letter behavior
- Add dashboard with status filters
- Add polling updates in UI

Deliverable:

- End-to-end lifecycle visible in dashboard

## Week 5: Hardening

- Add tests for auth and scheduling flows
- Add structured logs and metrics
- Add CI pipeline and deployment scripts
- Create runbooks and DR validation

Deliverable:

- Stable demo-ready system with operations docs
