# Worker Service

Dedicated worker process that consumes scheduled publish jobs from Redis and updates MongoDB status.

## Run

```bash
uv sync
uv run python -m src.worker
```
