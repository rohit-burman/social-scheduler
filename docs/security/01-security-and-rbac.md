# Security and RBAC Guide

## Security Principles

- Never trust client role claims
- Enforce workspace boundary on every query
- Encrypt secrets at rest and in transit
- Log security-relevant events

## RBAC Matrix

### Owner

- Full workspace control
- Invite/remove members
- Change roles
- Manage provider connections
- Create/edit/schedule/retry posts

### Editor

- Create/edit/schedule/retry posts
- View job logs
- Cannot manage membership roles

### Viewer

- Read-only access to workspace content
- Cannot create or edit posts
- Cannot trigger schedule/retry actions

## JWT and Session Design

- Short-lived access token (15 minutes)
- Long-lived refresh token (7-30 days)
- Refresh rotation with token family invalidation on reuse

## Password Policy

- Minimum 10 characters
- Require mixed character classes
- Hash with bcrypt/argon2 (cost tuned for environment)

## Input and Upload Validation

- Validate MIME and extension both
- Limit upload size by media type
- Sanitize filename and use generated storage key

## API Hardening

- CORS strict allowlist
- Rate limiting on auth and publish endpoints
- Request ID and structured logs
- Security headers at reverse proxy

## Secret Management

- Local: `.env` only for development
- Production: secret manager or platform secrets
- Never store secrets in repo

## Audit Events

Log at minimum:

- login success/failure
- token refresh and revocation
- role changes
- provider connect/disconnect
- schedule/retry actions
- publish success/failure
