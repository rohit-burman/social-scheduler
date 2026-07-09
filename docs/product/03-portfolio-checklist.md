# Portfolio and Interview Checklist

## Project Readiness

- [ ] Public repository with clean README
- [ ] Architecture diagram included
- [ ] API and worker separation explained
- [ ] Screenshots or short demo video
- [ ] Deployment URL available

## Engineering Signals

- [ ] Auth with refresh rotation
- [ ] Workspace RBAC enforced server-side
- [ ] Queue retries and dead-letter strategy
- [ ] Audit logs for publish attempts
- [ ] CI checks and release process documented

## Demo Script

1. Login and create workspace
2. Connect mock provider
3. Create draft with media
4. Schedule post in future timezone
5. Show worker processing and final status
6. Show failed flow and retry behavior

## Resume Bullet Template

Built a social content scheduling platform using Next.js, FastAPI, MongoDB, and Redis with workspace RBAC, media uploads, delayed job queues, retries with backoff, and status dashboards for async publish workflows.
