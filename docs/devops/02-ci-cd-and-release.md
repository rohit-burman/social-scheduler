# CI/CD and Release Strategy

## Branching Model

- `main`: production-ready
- `develop`: integration branch
- feature branches: `feat/<name>`

## CI Pipeline Stages

1. Checkout and setup runtimes
2. Dependency install
3. Lint checks
4. Build checks
5. Unit/integration tests
6. Artifact build (optional)

## Suggested CD Flow

1. Merge to main
2. Build Docker images for web/api/worker
3. Push images to registry
4. Deploy to staging
5. Run smoke tests
6. Manual approval
7. Deploy to production

## Release Versioning

- Use SemVer tags: `vX.Y.Z`
- Keep release notes for every tag

## Rollback Strategy

- Keep previous image tags available
- One-click rollback in deployment platform
- Run post-rollback health validation

## Required CI Checks for PR

- web lint/build
- api lint/tests
- worker lint/tests
- docs lint (optional but recommended)
