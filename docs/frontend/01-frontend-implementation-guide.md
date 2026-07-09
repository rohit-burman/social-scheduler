# Frontend Implementation Guide (Next.js)

## Objective

Build a practical SaaS-style dashboard with strong async state handling.

## Suggested Folder Structure

```text
apps/web/
  app/
    (auth)/
    (dashboard)/
      posts/
      calendar/
      jobs/
      settings/
  components/
    ui/
    forms/
    dashboard/
  features/
    auth/
    workspace/
    posts/
    jobs/
  lib/
    api-client.ts
    query-client.ts
    date.ts
    rbac.ts
  stores/
    workspace-store.ts
    modal-store.ts
```

## State Management Strategy

- Server state: TanStack Query
- Client UI state: Zustand
- Forms: React Hook Form + Zod

## Screens to Build

1. Login / signup
2. Workspace list and create flow
3. Invite members and role assignment
4. Compose post screen
5. Scheduler modal with timezone picker
6. Calendar view
7. Job status dashboard
8. Failed job details and retry action

## UX Requirements

- Show explicit status chips:
  - draft
  - scheduled
  - published
  - failed
- Disable edit/schedule buttons for Viewer role
- Show upload progress and failure messages
- Use optimistic update for schedule action
- Poll job status endpoint every 10-20 seconds

## API Client Rules

- Add auth token in request interceptor
- On 401, run refresh token flow once
- If refresh fails, redirect to login

## Suggested Milestone Order

1. Auth pages and protected route shell
2. Workspace switcher and role-aware nav
3. Draft list + compose form
4. Media upload integration
5. Schedule flow and optimistic updates
6. Status dashboard and polling
7. Error boundaries and empty states

## Definition of Done (Frontend)

- All MVP views complete
- RBAC behavior visible and correct
- Scheduling and status updates are smooth
- Critical flows covered by UI tests
