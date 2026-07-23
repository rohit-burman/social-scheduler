# Authentication Architecture

## Overview

This document describes the authentication system used by the backend
and the reasoning behind the design decisions. The goal is to provide a
production-inspired authentication flow that is simple enough for a
resume project while demonstrating security, scalability, and
maintainability.

------------------------------------------------------------------------

# Goals

-   Secure password storage
-   Stateless access tokens
-   Stateful refresh sessions
-   Refresh-token rotation
-   Replay (reuse) detection
-   Family revocation
-   Redis-backed login rate limiting
-   Clean separation of responsibilities

------------------------------------------------------------------------

# High-Level Flow

``` text
Register
    │
    ▼
Hash Password (Argon2id)
    │
    ▼
Store User
    │
    ▼
Login
    │
    ▼
Redis Rate Limit Check
    │
    ▼
Verify Password
    │
    ▼
Issue Token Pair
 ┌───────────────┐
 │ Access Token  │ 15 min
 │ Refresh Token │ 7 days
 └───────────────┘
    │
    ▼
Hash Refresh Token
    │
    ▼
Store Refresh Session
```

------------------------------------------------------------------------

# Project Structure

``` text
src/
├── api/
├── core/
│   └── security.py
├── db/
│   ├── mongodb.py
│   ├── indexes.py
│   └── repositories.py
├── models/
│   ├── user.py
│   └── auth.py
├── services/
│   ├── auth.py
│   └── rate_limit.py
└── settings.py
```

------------------------------------------------------------------------

# Responsibilities

## Routes

Responsible for:

-   HTTP request/response
-   Status codes
-   Dependency injection
-   Validation
-   Calling services

Should **not**:

-   Hash passwords
-   Build JWTs
-   Access MongoDB directly
-   Contain business rules

------------------------------------------------------------------------

## AuthService

Responsible for:

-   Register
-   Authenticate
-   Issue token pair
-   Rotate refresh token
-   Coordinate repositories
-   Coordinate security helpers

Acts as the orchestration layer.

------------------------------------------------------------------------

## security.py

Contains security primitives only.

Examples:

-   hash_password()
-   verify_password()
-   create_access_token()
-   create_refresh_token()
-   decode_token()
-   hash_token()

It should **not** know about MongoDB.

------------------------------------------------------------------------

## Repositories

Responsible only for persistence.

Examples:

-   create user
-   find by email
-   create refresh session
-   revoke family
-   rotate refresh session

No business rules.

------------------------------------------------------------------------

# Password Storage

Algorithm:

-   Argon2id (pwdlib recommended configuration)

Reason:

-   Designed for password hashing
-   Memory hard
-   Resistant to GPU attacks

Passwords are never encrypted.

They are hashed.

------------------------------------------------------------------------

# JWT Design

## Access Token

Claims:

``` json
{
  "sub": "<user_id>",
  "type": "access",
  "jti": "...",
  "iat": "...",
  "exp": "..."
}
```

Lifetime:

15 minutes

Used for:

Authenticated API requests.

------------------------------------------------------------------------

## Refresh Token

Claims:

``` json
{
  "sub": "<user_id>",
  "type": "refresh",
  "jti": "...",
  "family_id": "...",
  "iat": "...",
  "exp": "..."
}
```

Lifetime:

7 days

Used only for:

POST /auth/refresh

------------------------------------------------------------------------

# Why Two Tokens?

Access tokens:

-   Short-lived
-   Stateless
-   Cheap to validate

Refresh tokens:

-   Long-lived
-   Stored as server-side sessions
-   Can be revoked
-   Can detect replay

------------------------------------------------------------------------

# Refresh Session Schema

Collection:

refresh_sessions

``` text
_id
user_id
jti
family_id
token_hash
expires_at
used_at
revoked_at
replaced_by_jti
created_at
```

## Field Meaning

  Field             Purpose
  ----------------- ------------------------------------
  user_id           Owner of session
  jti               Unique token identifier
  family_id         Rotation chain identifier
  token_hash        SHA-256 of refresh token
  expires_at        Expiration timestamp
  used_at           First successful refresh
  revoked_at        Administrative/security revocation
  replaced_by_jti   Next refresh token
  created_at        Audit timestamp

------------------------------------------------------------------------

# Refresh Token Rotation

``` text
Login

↓

R1

↓

Refresh

↓

R2

↓

Refresh

↓

R3
```

Each refresh token can be successfully used only once.

------------------------------------------------------------------------

# Reuse Detection

Normal:

``` text
R1

↓

Rotate

↓

R2
```

Attack:

``` text
Attacker uses R1 again

↓

R1 already consumed

↓

Reuse detected

↓

Revoke family

↓

R2 becomes invalid
```

------------------------------------------------------------------------

# Login Rate Limiting

Storage:

Redis

Key:

``` text
rate_limit:login:failure:<ip>:<email>
```

Window:

15 minutes

Policy:

-   5 failed attempts allowed
-   Subsequent attempts receive 429

Implementation:

Redis Lua Script

``` text
INCR

↓

if first increment

↓

EXPIRE

↓

return count
```

Reason:

Avoid race condition between INCR and EXPIRE.

------------------------------------------------------------------------

# Authentication Dependency Flow

``` text
HTTP Request

↓

Authorization: Bearer <JWT>

↓

OAuth2PasswordBearer

↓

decode_token()

↓

Validate type == access

↓

Load User

↓

Verify active

↓

CurrentUserDep

↓

Protected Endpoint
```

------------------------------------------------------------------------

# MongoDB Indexes

Users

-   email (unique)

Refresh Sessions

-   jti (unique)
-   expires_at (TTL)
-   family_id
-   user_id

------------------------------------------------------------------------

# Security Decisions

## Why store SHA-256 of refresh token?

Database compromise should not expose usable refresh credentials.

------------------------------------------------------------------------

## Why not store passwords with SHA-256?

Passwords have low entropy.

Argon2id is intentionally expensive.

------------------------------------------------------------------------

## Why store sessions in MongoDB?

Needed for:

-   logout
-   rotation
-   revocation
-   replay detection

------------------------------------------------------------------------

# Testing Checklist

## Registration

-   User created
-   Password hashed
-   Duplicate email rejected

## Login

-   Valid credentials
-   Invalid credentials
-   Rate limiting

## Access Token

-   Valid
-   Expired
-   Invalid signature
-   Wrong type

## Refresh

-   Rotation succeeds
-   Old refresh rejected
-   Reuse revokes family
-   Revoked family rejected

------------------------------------------------------------------------

# Future Enhancements

-   HttpOnly refresh cookies
-   CSRF protection
-   Device/session metadata
-   Absolute session lifetime
-   Multiple device management
-   Audit log UI
-   Key rotation (kid)
-   Asymmetric JWT signing (RS256/EdDSA)

------------------------------------------------------------------------

# Interview Talking Points

-   Difference between Authentication and Authorization
-   Why Argon2id instead of SHA-256 for passwords
-   Why SHA-256 for refresh-token hashing
-   Why Access + Refresh tokens
-   Stateless vs Stateful authentication
-   Why JWT contains `type`
-   Why `jti` exists
-   Why `family_id` exists
-   Refresh-token rotation
-   Replay detection
-   Redis atomic `INCR`
-   Lua scripting for atomic `INCR + EXPIRE`
-   MongoDB single-document atomic updates
-   Why repositories should not contain business logic
-   Why services orchestrate multiple repositories

------------------------------------------------------------------------

# Current Status

✅ Registration

✅ Password hashing

✅ Login

✅ Redis rate limiting

✅ JWT authentication

✅ Access token

✅ Refresh token

✅ Refresh-token rotation

✅ Replay detection

✅ Family revocation

✅ Protected endpoints

Next phase:

Workspace isolation → Membership → RBAC → Posts → Scheduler → Workers
