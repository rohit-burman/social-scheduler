# Project Overview: Social Content Automation Scheduler

## At a Glance

| Aspect | Details |
|--------|---------|
| **Type** | Fullstack SaaS product with async job processing |
| **Duration** | 5 weeks (25 days) phased development |
| **Team** | Solo or small team (1-3 developers) |
| **Difficulty** | Intermediate+ (production patterns required) |
| **Stack** | Next.js + FastAPI + MongoDB + Redis |

## What You're Building

A **workspace-based social content scheduler** where:

```
User creates draft post
    ↓
Invites team members with roles (Owner/Editor/Viewer)
    ↓
Compose post with text + media (images/videos)
    ↓
Schedule for future date/time with timezone support
    ↓
Background worker publishes at scheduled time
    ↓
Provider succeeds → post published ✅
    or
    Provider fails → auto-retry with backoff ↻
    ↓
Dashboard shows real-time status for all posts
```

## Core Features You'll Implement

### 1. **Authentication & Team** (Week 1)
- Sign up and login securely
- Refresh token rotation (prevent token reuse attacks)
- Create workspace
- Invite team members
- Assign roles: Owner, Editor, Viewer
- Enforce permissions on every API call

### 2. **Content Creation** (Week 2)
- Rich text composer
- Media upload (images/videos)
- Save drafts and edit anytime
- List all drafts with filters
- Validate file types and sizes

### 3. **Scheduling & Publishing** (Week 3)
- Pick date, time, and timezone
- Validate it's in the future
- Background worker picks up jobs
- Simulated social provider calls
- Track success/failure

### 4. **Reliability & Visibility** (Week 4)
- Automatic retry on failure (5 times by default)
- Exponential backoff (30s, 60s, 120s, ...)
- Mark as permanent failed after max retries
- Dashboard shows all posts by status
- Real-time polling updates
- View attempt history and error details

### 5. **Operations & Testing** (Week 5)
- Unit and integration tests
- Security hardening
- Monitoring and alerting
- Deployment documentation
- Runbook for common incidents

## Why This Project Matters

### ✨ Shows Real Skills
- **Async Processing**: Why background jobs exist and how to make them reliable
- **Distributed Systems**: How to make jobs work without losing data
- **Team Features**: RBAC prevents one user from accessing another's workspace
- **Retry Strategy**: How to recover gracefully from failures
- **Data Modeling**: Document DB (MongoDB) flexibility vs. relational constraints

### 💼 For Interviews
- Demonstrates you can build **complete products**, not just CRUD apps
- Shows understanding of **reliability patterns** (retries, queues, audits)
- Proves **multi-tenancy** and security thinking (RBAC, workspace isolation)
- Portfolio-ready: Shows **async state management** on frontend and backend

### 🎓 For Learning
- Learn **queue systems** (Redis) and when they're necessary
- Understand **token-based auth** and session management
- Practice **role-based access control** (server-side enforcement)
- Experience **testing async code** (jobs, retries, polling)

## Data You'll Manage

```
MongoDB Collections:
├── users (email, password hash, display name)
├── workspaces (name, owner, created date)
├── workspace_members (user, workspace, role)
├── provider_connections (workspace, provider type, account name)
├── posts (workspace, content, media, status, scheduled time)
├── publish_jobs (post ID, queue ID, status, attempt count)
├── publish_attempts (audit trail: request, response, duration, timestamp)
└── refresh_tokens (user, token hash, family ID, expiry)

Redis Data:
├── publish:scheduled (delayed job queue)
└── publish:dead-letter (permanent failures)
```

## System Behavior Examples

### Example 1: Happy Path
```
1. Editor creates draft "Happy Monday!" with 2 images
2. Editor schedules for tomorrow 9 AM India time
3. Converts to UTC (3:30 AM) and stores in MongoDB
4. Redis enqueues job with 24-hour delay
5. Next morning, worker wakes up and calls mock Twitter API
6. API returns 200 OK with tweet ID
7. Worker updates post status to "published"
8. Dashboard shows post moved to "Published" tab
9. User sees "Published 1 hour ago"
```

### Example 2: Failure with Retry
```
1. Editor schedules post for 3 PM
2. At 3 PM, worker calls mock provider
3. API returns 500 error (simulating provider outage)
4. Worker logs attempt #1 as failed
5. Worker calculates next retry: 3 PM + 30 seconds = 3:00:30 PM
6. Job re-enqueued with 30-second delay
7. After 30 seconds, worker retries (attempt #2)
8. Still fails with timeout error
9. Worker calculates next retry: 3:00:30 PM + 60 seconds = 3:01:30 PM
10. Pattern repeats until attempt #5 succeeds or max attempts hit
11. If max attempts (5) hit and still failing:
    - Status becomes "Failed"
    - Job moved to dead-letter queue
    - User sees "Failed after 5 attempts" in dashboard
    - User can click "Retry" button to try again
```

### Example 3: RBAC in Action
```
1. Owner creates workspace "Acme Co"
2. Owner invites Editor (Sarah) and Viewer (John)
3. Sarah (Editor):
   - POST /posts → ✅ 201 Created
   - POST /posts/{id}/schedule → ✅ 202 Accepted
   - PATCH /workspaces/{id}/members/{memberId} → ❌ 403 Forbidden
4. John (Viewer):
   - GET /posts → ✅ 200 OK (read-only)
   - POST /posts → ❌ 403 Forbidden
   - GET /jobs → ✅ 200 OK (read-only)
   - POST /posts/{id}/retry → ❌ 403 Forbidden
5. Owner:
   - Everything works
```

## Key Files You'll Create

### Backend
```
apps/api/src/
├── main.py (FastAPI app)
├── settings.py (config from env)
├── api/
│   └── routes/
│       ├── auth.py (signup, login, refresh, logout)
│       ├── workspaces.py (create, list, invite)
│       ├── posts.py (create, list, update)
│       └── jobs.py (status, retry)
├── domain/
│   ├── auth/ (token logic)
│   ├── rbac/ (permission checks)
│   └── scheduling/ (queue enqueue)
├── infra/
│   ├── mongodb/ (data access)
│   ├── redis/ (queue)
│   └── storage/ (media upload)
└── schemas/ (pydantic models)

apps/worker/src/
├── worker.py (consumer loop)
├── queue/ (redis polling)
├── publish/ (execute publish)
└── providers/ (mock provider adapter)
```

### Frontend
```
apps/web/app/
├── (auth)/
│   ├── signup/page.tsx
│   └── login/page.tsx
├── (dashboard)/
│   ├── layout.tsx
│   ├── posts/page.tsx
│   ├── composer/page.tsx
│   └── jobs/page.tsx
└── layout.tsx (app shell with auth guard)

apps/web/components/
├── auth/ (login form, signup form)
├── composer/ (rich editor, media upload)
├── scheduler/ (date/time/timezone picker)
├── dashboard/ (status filters, job list)
└── ui/ (form controls, buttons, modals)
```

## Milestones & Checkpoints

| Week | Milestone | What's Working |
|------|-----------|-----------------|
| 1 | Foundation | Sign up → create workspace → invite team |
| 2 | Content | Create posts → upload media → edit drafts |
| 3 | Scheduling | Schedule posts → worker publishes → see status |
| 4 | Reliability | Retries work → failed posts visible → manual retry |
| 5 | Operations | Tests pass → docs complete → demo ready |

## Success Looks Like

- ✅ You can go from signup to published post in < 5 minutes
- ✅ Failed posts automatically retry and eventually publish
- ✅ Dashboard updates status in real-time without page refresh
- ✅ Different roles see different UI/permissions
- ✅ Worker survives restart without losing jobs
- ✅ Complete audit trail of all publish attempts
- ✅ Team can collaborate on workspace safely (no data leaks)
- ✅ All critical flows covered by tests
- ✅ Ops docs explain how to deploy, monitor, and recover

## What Makes This Different from CRUD App

| Aspect | Typical CRUD | This Project |
|--------|------------|--------------|
| Persistence | Sync writes to DB | Async jobs in queue |
| Error Recovery | User retries | Auto-retry with backoff |
| Team Features | Basic auth | Full RBAC with audit |
| Data Isolation | None | Full workspace isolation |
| Testing | Unit tests | Async + integration tests |
| Monitoring | Logs | Metrics + alerting |
| Operations | Deploy app | Deploy app + worker + queue |

## Time Estimate Breakdown

| Phase | Focus | Est. Days | Est. Hours |
|-------|-------|----------|-----------|
| 1 | Auth + Workspace + RBAC | 5 | 40 |
| 2 | Posts + Media Upload | 5 | 40 |
| 3 | Scheduling + Queue + Worker | 5 | 50 |
| 4 | Reliability + Dashboard | 5 | 50 |
| 5 | Tests + DevOps + Docs | 5 | 50 |
| **Total** | **Full MVP** | **25** | **230** |

Working ~2 hours/day: 115 days part-time
Working ~8 hours/day: 29 days full-time

## Next Steps

1. Read [docs/00-index.md](../00-index.md) for reading order
2. Start with [docs/architecture/01-system-overview.md](../architecture/01-system-overview.md)
3. Follow the weekly phases checklist in this document
4. Use the detailed acceptance criteria for testing

---

**Bottom line**: This is a real product with real reliability concerns. By the end, you'll have built something that looks simple but demonstrates understanding of how to make async systems trustworthy.
