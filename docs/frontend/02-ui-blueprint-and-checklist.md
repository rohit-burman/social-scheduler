# Frontend UI Blueprint and Checklist

## App Shell

- [ ] Protected layout with auth guard
- [ ] Workspace switcher in top nav
- [ ] Role badge for active membership

## Auth

- [ ] Signup page
- [ ] Login page
- [ ] Session refresh handling
- [ ] Logout action

## Workspace

- [ ] Workspace list and create modal
- [ ] Member list table
- [ ] Invite flow
- [ ] Role update controls (Owner only)

## Composer

- [ ] Rich text input
- [ ] Media upload widget with progress
- [ ] Provider selection
- [ ] Draft save feedback

## Scheduler

- [ ] Date and time picker
- [ ] Timezone selector
- [ ] Validation for past dates
- [ ] Optimistic status transition to scheduled

## Dashboard

- [ ] Status tabs: draft/scheduled/published/failed
- [ ] Filter by provider and date range
- [ ] Job detail drawer with attempt history
- [ ] Retry button for failed posts

## Async UX

- [ ] Polling strategy with adaptive interval
- [ ] Background refresh indicator
- [ ] Toast notifications on status change
- [ ] Graceful API error boundaries

## Quality

- [ ] Unit tests for form and role guard
- [ ] Integration tests for compose/schedule
- [ ] e2e smoke for login-to-publish
