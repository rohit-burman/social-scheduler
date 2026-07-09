# Testing Strategy

## Testing Pyramid

1. Unit tests
2. Integration tests
3. End-to-end tests

## Backend Test Scope

### Unit

- Auth token generation and validation
- RBAC guard decisions
- Retry delay calculations
- State transition validator

### Integration

- Schedule endpoint inserts job + queue message
- Worker consumes job and writes attempt log
- Failed attempts retry and become terminal after max

### Contract

- API response schema validation with golden fixtures

## Frontend Test Scope

### Unit

- Form validation rules
- Role-based UI guards
- Status badge mapping

### Integration

- Compose + schedule flow with mocked API
- Polling updates status transitions

### E2E (Playwright)

- Login -> create workspace -> create post -> schedule -> see published/failed

## Test Data Strategy

- Seed fixed users and workspaces
- Seed deterministic posts for status filters
- Use explicit clock control for schedule tests where possible

## Quality Gates

- No merge if lint fails
- No merge if backend integration suite fails
- No merge if critical e2e smoke test fails

## Minimum Coverage Targets

- Backend domain logic: 80%
- Frontend feature modules: 70%
- Critical flows (auth/schedule/publish): mandatory tests regardless of percentage
