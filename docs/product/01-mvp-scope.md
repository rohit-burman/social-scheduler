# MVP Scope and Product Requirements

## Executive Summary

**Social Content Automation Scheduler** is a fullstack SaaS product that enables solo creators and small agency teams to compose, schedule, and publish social media content across mock providers with automatic retries, status tracking, and team collaboration via workspace RBAC.

The project demonstrates production-grade patterns: workspace isolation, async job processing with queues, failure recovery, audit trails, and realtime status updates.

## Problem Statement

Content creators and agency teams waste time managing multiple social platform interfaces. They need a unified scheduling interface where:
- Team members can collaborate on content
- Posts can be scheduled across multiple mock providers
- Publication status is tracked reliably
- Failed publishes can be retried with clear error visibility
- Team members have role-based access control

## Solution Overview

A web-based workspace that centralizes social content scheduling:

1. **Unified Composer**: Create posts with rich text and media attachments once
2. **Smart Scheduling**: Timezone-aware scheduling with future datetime validation
3. **Reliable Publishing**: Background job queue with automatic retries and failure handling
4. **Status Visibility**: Real-time dashboard showing draft/scheduled/published/failed states
5. **Team Collaboration**: Workspace membership with role-based access control
6. **Audit Trail**: Complete history of publish attempts and state transitions

## Product Vision

A team workspace where social content moves through a clear lifecycle:

```
draft → scheduled → publishing → published
                         ↓
                       failed (with retry)
```

## Target Users

### Primary
- **Solo Creators**: Content creators managing multiple social accounts
- **Small Agencies**: 2-10 person teams managing client accounts
- **Community Managers**: Managing brand presence across channels

### Secondary
- **Junior Developers**: Learning async patterns, queues, RBAC, and realtime updates
- **Portfolio Builders**: Demonstrating fullstack capability with production concerns

## MVP Features (Must Have)

### Authentication & Security
1. **Email/Password Signup**: Self-service registration with email validation
2. **Secure Login**: Password hashing with bcrypt, rate limiting on failed attempts
3. **Token Rotation**: Short-lived access tokens + long-lived refresh tokens with family-based revocation
4. **Session Management**: Refresh token rotation prevents token reuse attacks
5. **Logout**: Revoke all active refresh token families

### Workspace Management
6. **Create Workspace**: Owner becomes admin of new workspace
7. **Invite Members**: Owner can invite team members via email
8. **Accept Invite**: Members accept invitations and join workspace
9. **Role Assignment**: Owner assigns roles (Owner, Editor, Viewer) to members
10. **Member List**: View all workspace members and their roles

### Provider Integration (Mock)
11. **Mock OAuth Flow**: Simulate social provider OAuth connection (no real tokens stored)
12. **Provider Connect**: Link mock social account (Twitter, LinkedIn, Instagram simulation)
13. **Provider Disconnect**: Revoke mock provider connection
14. **Account Validation**: Verify provider connection status before scheduling

### Post Composition
15. **Draft Post Creation**: Create new draft post with text content
16. **Rich Text Support**: Format text (bold, italic, links)
17. **Media Upload**: Upload images/videos with validation
18. **Multiple Media**: Attach multiple assets to single post
19. **Provider Metadata**: Store platform-specific options (hashtags, mentions)
20. **Draft Editing**: Modify draft until scheduled
21. **Save to Draft**: Auto-save and manual save functionality

### Scheduling
22. **Schedule Post**: Choose future date/time with timezone support
23. **Timezone Awareness**: Convert user-selected timezone to UTC
24. **Validate Future**: Prevent scheduling in the past
25. **Calendar Integration**: Visual calendar selector for date picking
26. **Retry Scheduling**: Reschedule failed published posts

### Background Processing
27. **Job Queue**: Redis-based queue with delayed job support
28. **Worker Process**: Dedicated process consuming scheduled jobs
29. **Provider Simulation**: Mock API calls with random success/failure
30. **Exponential Backoff**: Retry with increasing delays (30s, 60s, 120s, 240s, 480s)
31. **Max Retries**: Configurable max attempts (default 5)
32. **Dead Letter Queue**: Permanent failures moved to dead-letter for review
33. **Job Correlation**: Track attempts with request IDs

### Status Visibility
34. **Draft Dashboard**: Filter posts by draft status
35. **Scheduled Dashboard**: View upcoming scheduled posts
36. **Published Dashboard**: View successfully published posts
37. **Failed Dashboard**: View failed posts with error details
38. **Polling Updates**: Auto-refresh status every 10-20 seconds
39. **Job Details**: View detailed status and attempt history
40. **Error Messages**: Display failure reasons and retry attempts

### Audit & Logging
41. **Publish Attempts**: Log every attempt with request/response
42. **Status Audit Trail**: Immutable record of all state transitions
43. **User Actions**: Log create, schedule, retry actions
44. **Security Events**: Log login, role changes, provider connections

### RBAC (Role-Based Access Control)
- **Owner**: Full control, invite members, manage roles
- **Editor**: Create posts, schedule, view status, retry failed
- **Viewer**: Read-only access to workspace content

## Enhanced Features (Portfolio Plus)

These are optional additions after MVP that demonstrate deeper expertise:

### Calendar and Visualization
- Drag-and-drop calendar view for rescheduling
- Visual timeline showing scheduled publications
- Heatmap of posting activity by time/day

### Advanced Job Management
- Dead-letter queue UI for viewing permanent failures
- Manual replay of failed jobs with approval
- Bulk retry actions for multiple failed posts
- Job analytics: success rate by provider, time to publish

### Media Management
- Multi-image carousel post support
- Video thumbnail preview
- Image optimization and resizing
- Media asset library and reuse

### Webhooks and Callbacks
- Mock webhook callbacks from provider
- Webhook validation and signature verification
- Automatic status updates from provider callbacks
- Webhook delivery retry logic

### Analytics
- Basic stats: posts published, success rate
- Timeline chart: publications per day/week/month
- Provider performance comparison
- Failure analysis by error type

### AI Enhancements (Clearly Marked Optional)
- AI caption suggestion (clearly marked as bonus)
- Hashtag generation (clearly marked as bonus)
- Post tone analysis
- Best time to publish suggestions

## Technical Stack and Architecture

### Frontend
- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui (optional but recommended)
- **State Management**: 
  - Server state: TanStack Query (React Query)
  - Client UI state: Zustand
- **Forms**: React Hook Form + Zod validation
- **HTTP Client**: axios or fetch with middleware
- **Realtime**: Polling (MVP), WebSocket optional enhancement

### Backend API
- **Framework**: FastAPI with async/await
- **Language**: Python 3.12+
- **Web Server**: Uvicorn
- **API Docs**: Automatic OpenAPI/Swagger
- **Validation**: Pydantic v2
- **Task Queue**: Celery for distributed task processing

### Celery Worker Service
- **Task Queue**: Celery (distributed task queue)
- **Message Broker**: Redis
- **Result Backend**: Redis
- **Scheduler**: Celery Beat for periodic/delayed tasks
- **Monitoring**: Flower web dashboard
- **Language**: Python 3.12+

### Data Storage
- **Primary Database**: MongoDB (document flexibility for posts)
- **Message Broker & Result Backend**: Redis (Celery queue, retry logic, optional caching)
- **Object Storage**: Cloudflare R2 or local filesystem
  - Local for development
  - R2 for production with signed URLs

### DevOps & Deployment
- **Package Manager**: pnpm (JavaScript), uv (Python)
- **Monorepo Tool**: Turbo for build orchestration
- **Container**: Docker for each service
- **Composition**: Docker Compose for local dev
- **Orchestration**: Kubernetes ready (YAML templates provided)
- **IaC**: Terraform for Cloudflare R2
- **CI/CD**: GitHub Actions
- **Platforms**: Vercel (web), Railway/Render/Fly (API/Worker)

## Data Model Overview

### Core Entities

```
Users
├── Email (unique)
├── Password (hashed)
├── Display Name
└── Timestamps

Workspaces
├── Name & Slug (unique)
├── Owner User
├── Members (via workspace_members)
└── Timestamps

Workspace Members
├── User
├── Workspace
├── Role (owner|editor|viewer)
└── Invite Metadata

Provider Connections
├── Workspace
├── Provider Type (twitter|linkedin|instagram)
├── Account Name
├── Status (connected|error)
└── Encrypted Tokens

Posts
├── Workspace
├── Created By (User)
├── Provider Connection
├── Content (text + media array)
├── Status (draft|scheduled|publishing|published|failed)
├── Scheduled Time (UTC)
├── Timezone
├── Media Assets (keys + URLs)
├── Last Error
└── Timestamps

Publish Jobs
├── Post reference
├── Queue Job ID
├── Status (scheduled|running|retrying|succeeded|failed)
├── Attempt Counter
├── Next Retry Time
├── Scheduled At (UTC)
└── Timestamps

Publish Attempts (Audit)
├── Job reference
├── Attempt Number
├── Provider Request/Response
├── Success/Failure
├── Error Code & Message
├── Duration
└── Timestamp
```

## Key Requirements by Category

### Functional Requirements

**Authentication**
- Password minimum 10 chars with mixed classes
- Token refresh without re-login
- Secure logout revokes all sessions
- Rate limiting on login/auth endpoints

**Workspace**
- Each workspace is fully isolated (no cross-workspace data leaks)
- Members can be invited via email
- Roles control all create/schedule/delete permissions
- Audit log of membership changes

**Scheduling**
- Timezone-aware scheduling (accept any IANA timezone)
- Must validate scheduled time is in future
- Update allowed only for draft status
- Cancel should remove from queue if not yet running

**Publishing**
- Process exactly-once per job ID
- Retry only on retryable errors (network, timeout)
- Track every attempt with provider request/response
- Mark terminal failed after max attempts
- Move to dead-letter queue for manual review

**Media**
- Validate file type (image/video only by MIME)
- Validate file size (limit by type)
- Generate secure storage keys (UUID-based, not user input)
- Support local or R2 storage transparently

### Non-Functional Requirements

**Performance**
- API responses < 300ms P95 at baseline load
- Dashboard dashboard load < 2 seconds
- Polling updates within 20 second window
- Media upload progress visible (chunked or streaming)

**Reliability**
- Job queue survives service restarts (durability)
- Idempotent job processing (safe to retry)
- Graceful shutdown of worker (wait for in-flight)
- Dead-letter queue preserves all terminal failures

**Security**
- HTTPS in production
- CORS whitelist specific origins
- Input validation on all endpoints
- SQL/NoSQL injection prevention (use ORM/queries)
- CSRF tokens for stateful operations
- Rate limiting on sensitive endpoints
- Password hashing with bcrypt/argon2
- Secrets not in source code
- Audit log all sensitive actions

**Scalability**
- Horizontal scaling: multiple API and worker replicas
- Stateless design (no local session state)
- Database indexing for query performance
- Queue depth monitoring

**Observability**
- Structured JSON logs with request ID
- Correlation IDs for tracing job lifecycle
- Metrics: request latency, error rates, queue depth
- Traces: optional OpenTelemetry
- Alerts: publish failure spike, dead-letter growth

## User Personas

### Persona 1: Sarah (Solo Creator)
- **Age**: 28
- **Background**: Content creator managing 5 social accounts
- **Pain Point**: Spending 2 hours/day manually posting to each platform
- **Goal**: Bulk schedule weekly content at optimal times
- **Key Feature**: Timezone-aware scheduling, multi-channel publishing

### Persona 2: Marcus (Agency Owner)
- **Age**: 42
- **Background**: Runs 3-person social agency with 15 client accounts
- **Pain Point**: Managing across team, tracking what posted where, handling delays
- **Goal**: Team coordination with role-based control, visibility of failures
- **Key Feature**: RBAC, job status dashboard, audit logs

### Persona 3: Jamie (Junior Developer)
- **Age**: 23
- **Background**: Learning fullstack development, portfolio building
- **Pain Point**: Doesn't know production patterns (queues, RBAC, retries)
- **Goal**: Build demo project showing async patterns and team features
- **Key Feature**: Clean separation of concerns, documented architecture

## Detailed User Stories and Requirements

### Epic 1: Authentication & Account Management

**Story 1.1**: Sign Up
- As a new user, I can sign up with email and password
- I receive a confirmation email
- I can then log in immediately
- Password must meet complexity requirements
- Duplicate email is rejected

**Story 1.2**: Login & Session
- As a registered user, I can log in with email/password
- I'm issued an access token (short-lived) and refresh token (long-lived)
- Access token includes user ID and workspace list
- Failed login is rate-limited after 5 attempts
- I can log out and invalidate all refresh tokens

**Story 1.3**: Token Refresh
- As a logged-in user, my access token expires after 15 minutes
- I can use refresh token to get new access/refresh pair
- Old refresh token is revoked, new family ID issued
- If refresh is replayed, entire family is invalidated
- Refresh can only succeed once per token

### Epic 2: Workspace Setup and Team

**Story 2.1**: Create Workspace
- As a user, I can create a new workspace with a name
- Name is unique (slug-ified for URLs)
- I automatically become the owner
- Workspace is ready to use immediately

**Story 2.2**: Invite Members
- As an owner, I can invite a team member by email
- Invitee receives email with join link
- Invitee can accept and join workspace
- I can see pending invitations
- I can revoke an invite before acceptance

**Story 2.3**: Manage Roles
- As an owner, I can see all members and their roles
- I can change a member's role (owner/editor/viewer)
- I cannot remove the last owner
- Role changes are audited with timestamp
- Members see their role in the workspace

**Story 2.4**: Remove Members
- As an owner, I can remove a member from workspace
- Removed member loses all access immediately
- Their posts remain but can't be edited by them
- Removal is audited

### Epic 3: Social Provider Integration

**Story 3.1**: Connect Mock Provider
- As an editor, I can connect a mock social account
- I choose provider type (Twitter/LinkedIn/Instagram)
- I enter account name/handle
- Connection is validated and status shown
- Token is stored encrypted

**Story 3.2**: Manage Connections
- As an editor, I can see all connected accounts
- I can disconnect an account
- Disconnected account can't be used for new posts
- Already-scheduled posts keep reference but fail gracefully

### Epic 4: Content Creation

**Story 4.1**: Create Draft Post
- As an editor, I can create a new draft post
- I select a provider connection
- I write post content (text only, MVP)
- Post is saved as draft
- I can see a list of my drafts

**Story 4.2**: Edit Draft
- As an editor, I can edit a draft post
- I can change text content
- I can add/remove media
- Changes are auto-saved or manually saved
- Cannot edit after scheduling

**Story 4.3**: Upload Media
- As an editor, I can upload images or videos to a post
- File must be image or video MIME type
- File size is validated per type
- Upload shows progress indicator
- Media is persisted to local or R2 storage
- Media URL is generated for post

**Story 4.4**: View Media
- As a user, I can see uploaded media previewed in composer
- I can remove media from post
- Media shows file size and type

### Epic 5: Scheduling & Publishing

**Story 5.1**: Schedule Post
- As an editor, I can schedule a post
- I select date/time and timezone
- UI converts to UTC for storage
- API validates time is in future
- Post status changes to `scheduled`
- Job is enqueued in Redis queue

**Story 5.2**: View Scheduled Posts
- As a user, I can see all scheduled posts in dashboard
- I can filter by provider
- I can filter by date range
- I can sort by scheduled time
- Each post shows next scheduled attempt

**Story 5.3**: Automatic Publishing
- As a user, I expect posts to publish at scheduled time
- Worker wakes up and runs due jobs
- Provider is called with post payload
- Success/failure is recorded
- Status updates visible within polling interval

**Story 5.4**: Handle Publish Failure
- As the system, if publish fails:
  - Failure is recorded with error code
  - Job is requeued with exponential backoff
  - Next retry time is calculated
  - Attempt count increments
- If max attempts reached:
  - Status becomes `failed`
  - Job moved to dead-letter queue
  - User can see failure details

**Story 5.5**: Manual Retry
- As an editor, I can manually retry a failed post
- I can see retry button on failed jobs
- Clicking retry enqueues new job
- Retry uses fresh attempt counter
- New attempt is logged

### Epic 6: Status & Monitoring

**Story 6.1**: Dashboard Overview
- As a user, I see dashboard with status counts
- Drafts: posts not yet scheduled
- Scheduled: upcoming publishes
- Published: successful publishes
- Failed: terminal failures
- Each tab shows count and list

**Story 6.2**: Job Status Details
- As a user, I can click a post to see details
- I see current status
- I see scheduled/published/failed time
- I see all attempts with timestamps
- I see provider request/response (sanitized)
- I see error message if failed

**Story 6.3**: Polling Updates
- As a user viewing dashboard:
  - Status updates automatically every 15 seconds
  - Published posts move to published tab
  - Failed posts appear in failed tab
  - Attempt counter updates
  - No page refresh needed

**Story 6.4**: Audit Log
- As an owner, I can view audit log
- Logs show: who did what, when, from where
- Actions: created, scheduled, retried, published, failed
- Logs cannot be modified
- Logs retained for 90 days

### Epic 7: Role-Based Access Control

**Story 7.1**: Editor Permissions
- As an editor, I can:
  - Create and edit drafts
  - Schedule posts
  - Retry failed posts
  - View status dashboard
  - Connect providers
- As an editor, I cannot:
  - Invite members
  - Change roles
  - Delete other's posts
  - View audit logs

**Story 7.2**: Viewer Permissions
- As a viewer, I can:
  - View draft/scheduled/published/failed posts
  - View job status and attempts
  - View provider connections
- As a viewer, I cannot:
  - Create posts
  - Schedule posts
  - Upload media
  - Connect providers
  - Manage team

**Story 7.3**: Owner Permissions
- As an owner, I can:
  - Do everything editors can do
  - Invite/remove members
  - Change member roles
  - View audit logs
  - Delete workspace

## Detailed Acceptance Criteria

### Authentication & Authorization

- [ ] Signup with email and password creates new user with hashed password
- [ ] Login with invalid password returns 401 after rate-limiting
- [ ] Access token is issued with 15-minute expiry
- [ ] Refresh token is issued with 7-day expiry
- [ ] Refresh endpoint returns new token pair and invalidates old refresh token
- [ ] Logout revokes all refresh tokens in the family
- [ ] Protected endpoints reject requests without valid access token
- [ ] Protected endpoints reject requests with expired access token

### Workspace Isolation

- [ ] User cannot access workspace without being a member
- [ ] User cannot see posts from other workspaces
- [ ] Queries automatically filtered by workspace ID on backend
- [ ] API returns 403 for cross-workspace access attempts
- [ ] Audit logs show every cross-workspace access attempt

### Role-Based Access Control

- [ ] Editor can create and schedule posts
- [ ] Viewer cannot create posts (403 on POST /posts)
- [ ] Viewer cannot schedule (403 on POST /schedule)
- [ ] Viewer can read posts and job status (200 OK)
- [ ] Owner can invite members and change roles
- [ ] All role checks happen server-side (client UI is UX only)
- [ ] Removing role immediately revokes permissions
- [ ] Orphaned resources from removed user are handled gracefully

### Post Composition

- [ ] Post can be created with text content only
- [ ] Media files are validated by MIME type
- [ ] Media files are validated by size (max configurable)
- [ ] Media is stored with UUID key (not user-supplied name)
- [ ] Draft post can be edited until scheduled
- [ ] Post status transitions are logged
- [ ] Attempting to edit scheduled post returns 409 Conflict

### Scheduling and Queue

- [ ] Scheduling validates datetime is in future (in UTC)
- [ ] Timezone parameter is converted to UTC correctly
- [ ] Invalid timezone is rejected with 400 Bad Request
- [ ] Scheduled post status changes to `scheduled`
- [ ] Job is enqueued in Redis with correct delay
- [ ] Job payload includes all required fields for worker

### Worker Processing

- [ ] Worker starts without errors
- [ ] Worker consumes jobs from queue
- [ ] Worker calls provider adapter
- [ ] Worker logs every attempt with timestamp
- [ ] Successful publish sets post status to `published`
- [ ] Failed publish sets status to `failed` if max attempts reached
- [ ] Retry is scheduled with exponential backoff formula: base * 2^(attempt-1)
- [ ] Default base delay is 30 seconds
- [ ] Max attempts is configurable (default 5)
- [ ] Worker gracefully shuts down after in-flight job completes

### Provider Simulation

- [ ] Mock provider randomly succeeds/fails
- [ ] Provider request includes post content and media URLs
- [ ] Provider response includes success/failure indicator
- [ ] Failed response includes error code and message
- [ ] Failure is logged with sanitized request/response (no secrets)

### Status Visibility

- [ ] Dashboard shows correct counts per status
- [ ] Dashboard filters work: by status, by provider, by date
- [ ] Job detail view shows all attempts
- [ ] Attempt view shows request, response, duration, timestamp
- [ ] Failed job shows error message and retry button
- [ ] Published job shows published timestamp

### Polling and Updates

- [ ] Frontend polls status endpoint every 10-20 seconds
- [ ] Published post appears in dashboard within 2 polling intervals
- [ ] Status updates without full page reload
- [ ] Polling stops if page is hidden (performance optimization)
- [ ] Network error in poll doesn't crash UI

### Audit Logging

- [ ] Every publish attempt is logged
- [ ] Audit log includes: who (user ID), what (action), when (timestamp), where (workspace)
- [ ] Status transitions are immutable (cannot be edited)
- [ ] Logs can be filtered by user and date range
- [ ] Sensitive data (tokens) is not logged

### Error Handling

- [ ] 400: Invalid input returns clear error message
- [ ] 401: Missing token returns 401 Unauthorized
- [ ] 403: Insufficient role returns 403 Forbidden
- [ ] 404: Missing resource returns 404 Not Found
- [ ] 409: Invalid state transition (e.g., edit scheduled post) returns 409 Conflict
- [ ] 500: Server error returns 500 with request ID for debugging
- [ ] All errors have consistent JSON schema with error code and message

### Data Integrity

- [ ] Database transactions ensure consistency
- [ ] Failed insert rolls back completely
- [ ] Job idempotency key prevents duplicate publishes
- [ ] Concurrent edits to same post don't conflict
- [ ] Deleted provider connection doesn't orphan scheduled posts

### Performance

- [ ] API endpoint responses < 300ms P95 at baseline
- [ ] Media upload shows progress (chunked or streaming)
- [ ] Dashboard loads with <2 second load time
- [ ] Polling doesn't cause CPU spike
- [ ] Database queries use indexes on workspace + status + timestamp

### Security

- [ ] Passwords never logged
- [ ] Tokens never logged in plain text
- [ ] Rate limiting on /auth/login (max 5/minute per IP)
- [ ] Rate limiting on /schedule (max 100/minute per user)
- [ ] CORS allows only specified origins
- [ ] Input is validated before database query
- [ ] No SQL/NoSQL injection possible
- [ ] Secrets come from environment, not code
- [ ] Media uploads are validated before storage

## Success Metrics and Key Results

### Functional Success
- [ ] 100% of scheduled jobs result in either published or terminal failed state
- [ ] 0% unauthorized cross-workspace data access incidents
- [ ] 99% job completion rate (jobs don't get stuck in queue)
- [ ] All critical user flows (auth, schedule, publish, retry) have integration tests
- [ ] 0 data corruption incidents during development

### Performance Success
- [ ] API endpoints respond in < 300ms P95 at baseline load
- [ ] Dashboard loads in < 2 seconds
- [ ] Status updates visible within 30 seconds of publish completion
- [ ] Media uploads show progress and complete within 5 minutes for 100MB file
- [ ] Database query P95 latency < 100ms with proper indexing

### Reliability Success
- [ ] Worker can restart without losing in-flight jobs
- [ ] Retry policy successfully publishes >90% of retried jobs
- [ ] No duplicate publications on job requeue
- [ ] Dead-letter queue captures all terminal failures
- [ ] Service continues operating during database or cache issues (graceful degradation)

### Security Success
- [ ] Password hashing algorithm is bcrypt or argon2 (not plain)
- [ ] No passwords or tokens in logs or error messages
- [ ] Rate limiting prevents brute force attacks
- [ ] CORS prevents unauthorized origin access
- [ ] All secrets loaded from environment, not hardcoded

### Quality Success
- [ ] Unit test coverage > 80% for domain logic
- [ ] Integration tests for: auth, schedule, publish, retry flows
- [ ] E2E tests for critical path: login → create workspace → schedule → publish
- [ ] Code review checklist completed for all PRs
- [ ] Zero high-severity security findings in scan

## Operational Requirements

### Monitoring & Observability
- [ ] Structured JSON logs with request ID and user context
- [ ] Job correlation IDs for tracing through queue pipeline
- [ ] Metrics exported: request latency, error rates, queue depth
- [ ] Alerts configured for: publish failure spike, dead-letter growth, API latency
- [ ] Dashboard shows key metrics in real-time

### Deployment & Scaling
- [ ] Application runs as separate API and worker processes
- [ ] Both API and worker can scale horizontally (stateless)
- [ ] Health checks available for both services
- [ ] Readiness/liveness probes configured
- [ ] Graceful shutdown waits for in-flight work

### Backup & Disaster Recovery
- [ ] Automated MongoDB backups daily
- [ ] Automated Redis snapshots
- [ ] DR test documented and executed quarterly
- [ ] Recovery time objective (RTO) < 60 minutes
- [ ] Recovery point objective (RPO) < 15 minutes

### Compliance & Governance
- [ ] Audit logs retained for 90+ days
- [ ] Data deletion complies with privacy regulations
- [ ] User data export available on request
- [ ] Security policy documented and followed
- [ ] Change log maintained for all deployments

## Out of Scope (Explicitly Not MVP)

- **Real Social APIs**: This uses mock providers (no real Twitter/LinkedIn APIs)
- **Billing & Payment**: No subscription model, pricing, or payment processing
- **Enterprise Features**: 
  - SSO/SAML authentication
  - Advanced RBAC (custom roles)
  - IP whitelisting
  - Audit log encryption
- **Advanced Analytics**: 
  - Detailed post-level analytics
  - Performance trending
  - Predictive scheduling recommendations
- **Content Libraries**:
  - Draft templates
  - Content calendar planning tools
  - Asset management system
- **Multi-language**: Only English UI and docs
- **Mobile Apps**: Web-only (responsive, but not native iOS/Android)
- **Real Webhooks**: Mock webhooks for demo, not production provider webhooks
- **Complex Media**: 
  - Video streaming/transcoding
  - GIF creation
  - Multi-layer image editor
- **AI/ML**:
  - Automatic caption generation (if included, clearly marked as bonus)
  - Optimal posting time prediction
  - Content moderation
- **Social Listening**: No monitoring of mentions or sentiment
- **Competitor Analysis**: No comparative data

## Development Phases (5-Week Sprint)

### Phase 1: Foundation (Week 1)
**Focus**: Auth, workspace, RBAC infrastructure

**Backend**
- [ ] Setup FastAPI project structure
- [ ] Implement user signup/login/logout
- [ ] JWT token generation and validation
- [ ] Refresh token rotation with family invalidation
- [ ] Create workspace collection and API
- [ ] Create membership collection
- [ ] Implement RBAC dependency check middleware
- [ ] Setup MongoDB connection and migration strategy

**Frontend**
- [ ] Setup Next.js project structure
- [ ] Create signup and login pages
- [ ] Implement auth state management (Zustand)
- [ ] Setup API client with axios/fetch
- [ ] Implement token refresh interceptor
- [ ] Create workspace switcher
- [ ] Protected route wrapper

**Infrastructure**
- [ ] Docker Compose for local dev (MongoDB, Redis)
- [ ] Environment template (.env.example)
- [ ] Health check endpoints

**Deliverable**
- User can sign up → create workspace → invite member → see roles enforced
- API and worker start without errors
- Tests verify auth flow and RBAC guards

**Verification Checklist**
- [ ] Login/logout works
- [ ] Refresh token rotates correctly
- [ ] Cross-workspace access rejected
- [ ] Role checks work on simple endpoint
- [ ] Workspace selector appears and switches context

---

### Phase 2: Content Composition (Week 2)
**Focus**: Post CRUD, media upload, draft lifecycle

**Backend**
- [ ] Post model and collection design
- [ ] Create draft endpoint: POST /posts
- [ ] Update draft endpoint: PATCH /posts/{id}
- [ ] List posts endpoint: GET /posts (with filters)
- [ ] Media upload abstraction (local driver first)
- [ ] Presigned URL generation
- [ ] Post metadata validation (text length, media count)
- [ ] Role checks on post create/update

**Frontend**
- [ ] Compose form with TanStack Query
- [ ] Rich text editor integration
- [ ] Media upload widget with progress
- [ ] File validation (MIME, size)
- [ ] Auto-save draft functionality
- [ ] Draft list view with filters
- [ ] Edit existing draft

**Database**
- [ ] Create posts collection with indexes
- [ ] Create media storage drivers

**Deliverable**
- Editor can create draft → add media → save → edit → see in list
- Media persists to local storage
- Viewer role cannot create posts (UI disabled, API rejects)

**Verification Checklist**
- [ ] Draft creation stores in MongoDB
- [ ] Media upload works locally
- [ ] Concurrent edits don't corrupt data
- [ ] File size/type validation works
- [ ] List endpoint filters by status, provider, date

---

### Phase 3: Scheduling and Queue (Week 3)
**Focus**: Schedule endpoint, Redis queue, worker consumer

**Backend**
- [ ] Schedule endpoint: POST /posts/{id}/schedule
- [ ] Validate future datetime in UTC
- [ ] Timezone conversion utility
- [ ] Create publish_jobs collection
- [ ] Enqueue to Redis with delayed execution
- [ ] Worker consumer loop implementation
- [ ] Provider adapter with mock success/failure
- [ ] Job status endpoint: GET /jobs/{id}

**Worker**
- [ ] Redis consumer polling loop
- [ ] Job deserialization and validation
- [ ] Provider execution (mock provider calls)
- [ ] Status update to MongoDB
- [ ] Basic error handling and logging

**Frontend**
- [ ] Schedule modal with date/time picker
- [ ] Timezone selector
- [ ] Validate future datetime (client + server)
- [ ] Show scheduled posts in dashboard
- [ ] Poll job status every 15 seconds

**Database**
- [ ] Create publish_jobs collection
- [ ] Create publish_attempts collection for audit

**Deliverable**
- Editor schedules post → worker picks it up → status shows published/failed
- UI updates status without refresh
- Can see attempt history

**Verification Checklist**
- [ ] Scheduled post enqueues to Redis
- [ ] Worker consumes and processes jobs
- [ ] Status transitions visible in dashboard
- [ ] Provider random failure works
- [ ] Polling updates UI correctly

---

### Phase 4: Reliability and Visibility (Week 4)
**Focus**: Retry logic, failure handling, dashboard

**Backend**
- [ ] Retry policy: exponential backoff
- [ ] Track attempt count and max attempts
- [ ] Mark terminal failed after max attempts
- [ ] Dead-letter queue for permanent failures
- [ ] Audit attempt logs with request/response
- [ ] Implement job idempotency by jobId

**Worker**
- [ ] Implement retry scheduling
- [ ] Calculate next retry with backoff formula
- [ ] Handle non-retryable errors
- [ ] Log all attempt details
- [ ] Move to dead-letter on terminal failure

**Frontend**
- [ ] Dashboard with status tabs (draft/scheduled/published/failed)
- [ ] Job detail modal with attempt history
- [ ] Retry button on failed posts
- [ ] Error message display
- [ ] Provider metadata display

**Testing**
- [ ] Integration test: create → schedule → fail → retry → publish
- [ ] Test retry backoff formula
- [ ] Test idempotency on duplicate delivery

**Deliverable**
- Failed post retries automatically
- User can manually retry
- Dashboard shows all state transitions
- Audit log complete

**Verification Checklist**
- [ ] First failure triggers retry after 30s
- [ ] Second retry after 60s
- [ ] Terminal failure after max attempts
- [ ] Retry button works
- [ ] Attempt log shows all details
- [ ] Manual retry works

---

### Phase 5: Hardening (Week 5)
**Focus**: Tests, observability, security, ops docs

**Testing**
- [ ] Unit tests for auth, RBAC, scheduling
- [ ] Integration tests for all critical flows
- [ ] E2E test: signup → schedule → publish
- [ ] Test RBAC enforcement on all endpoints
- [ ] Test concurrency and race conditions

**Security**
- [ ] Input validation on all endpoints
- [ ] Rate limiting on auth, schedule endpoints
- [ ] Secret management from environment
- [ ] Secure headers and CORS configuration
- [ ] Sanitize logs (no passwords, tokens)

**Observability**
- [ ] Structured logging with request ID
- [ ] Job correlation IDs
- [ ] Metrics endpoint or exporter
- [ ] Error tracking and alerting setup
- [ ] Dashboard for key metrics

**Operations**
- [ ] Deployment guide and runbook
- [ ] Health check procedures
- [ ] Backup and restore procedures
- [ ] Scaling instructions
- [ ] Incident response guide

**DevOps**
- [ ] GitHub Actions CI pipeline
- [ ] Docker image building
- [ ] Deployment scripts
- [ ] Environment configuration management

**Deliverable**
- All acceptance criteria passed
- 80%+ test coverage on domain logic
- Operational documentation complete
- Ready for demo and deployment

**Verification Checklist**
- [ ] All tests passing on main branch
- [ ] Code review completed
- [ ] Security scan clean
- [ ] Deployment tested in staging
- [ ] Runbook tested once
- [ ] Demo script ready

---

## What This Project Demonstrates

### For Portfolio/Interviews

**Full-Stack Capability**
- Frontend state management (TanStack Query, Zustand)
- Backend API design and implementation
- Async job processing and reliability patterns

**Production Patterns**
- Workspace isolation and multi-tenancy fundamentals
- Role-based access control (RBAC) design and enforcement
- JWT token management with refresh rotation
- Queue-based async processing with retries

**Data Handling**
- Document database (MongoDB) schema design
- In-memory cache and queue (Redis) for reliability
- Idempotent job processing
- Audit trail and immutable event logging

**Reliability Engineering**
- Retry logic with exponential backoff
- Dead-letter queue for error recovery
- Graceful failure handling and user feedback
- Testing strategies for async systems

**DevOps and Operations**
- Docker containerization
- Kubernetes readiness for horizontal scaling
- CI/CD pipeline setup
- Observability and monitoring

### Engineering Decisions

This project teaches **real tradeoffs**:

1. **Queue vs. Immediate**: Why background jobs matter when API can't guarantee completion
2. **Retry Strategy**: How to avoid duplicate work while ensuring reliability
3. **State Machines**: Why immutable status transitions prevent bugs
4. **Testing Async Code**: How to make queues testable
5. **Multi-tenancy**: How to prevent cross-workspace data leaks

---

## Quick Reference

### Key Dates & Milestones
- **Start**: Day 1 of planning
- **Phase 1 Complete**: Day 5 (Foundation)
- **Phase 2 Complete**: Day 10 (Content)
- **Phase 3 Complete**: Day 15 (Scheduling)
- **Phase 4 Complete**: Day 20 (Reliability)
- **Phase 5 Complete**: Day 25 (Hardening)

### Key Configuration Values
- **Access Token TTL**: 15 minutes
- **Refresh Token TTL**: 7 days
- **Polling Interval**: 15-20 seconds
- **Retry Base Delay**: 30 seconds
- **Max Retry Attempts**: 5
- **Password Min Length**: 10 chars
- **Rate Limit Auth**: 5 attempts/minute per IP
- **Rate Limit Schedule**: 100 actions/minute per user

### Team Roles
- **Developer**: Builds all features end-to-end
- **Code Reviewer**: Reviews PRs before merge to main
- **QA**: Tests acceptance criteria
- **DevOps**: Maintains CI/CD and deployments

For solo developers: you handle all roles, using docs as checklist.

### Critical API Endpoints (by Phase)

**Phase 1**
- POST /auth/signup
- POST /auth/login
- POST /auth/refresh
- POST /auth/logout
- POST /workspaces
- GET /workspaces

**Phase 2**
- POST /posts
- PATCH /posts/{id}
- GET /posts
- POST /media/presign
- POST /media/complete

**Phase 3**
- POST /posts/{id}/schedule
- GET /jobs/{id}
- GET /jobs (list)

**Phase 4**
- POST /posts/{id}/retry
- GET /dashboard/summary

**Phase 5**
- GET /health
- GET /metrics

### Success Criteria Summary
- ✅ Users can sign up, create workspace, invite team
- ✅ Editors can compose, schedule, and monitor posts
- ✅ Worker publishes jobs automatically with retry
- ✅ Dashboard shows real-time status with polling
- ✅ RBAC enforced on all protected endpoints
- ✅ All core flows tested and working
- ✅ Operational docs and runbooks complete
