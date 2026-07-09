# Operations Runbook

## Health Checks

- API: `GET /health`
- Worker: process heartbeat log every 30s
- Redis: ping latency
- MongoDB: command ping

## Incident Severity Guide

- SEV-1: complete publish outage
- SEV-2: high failure rate or delayed publishes
- SEV-3: non-critical UI degradation

## Common Incident: Jobs Not Publishing

1. Check Redis queue depth
2. Check worker process health
3. Check provider error rate
4. Verify Mongo status transition logs

Mitigation:

- Restart worker deployment
- Reduce concurrency if provider rejects bursts
- Requeue dead-letter items manually after fix

## Common Incident: High Failed Publish Rate

1. Review latest `publish_attempts` errors
2. Classify retryable vs non-retryable
3. Validate provider adapter payload contract
4. Confirm token validity for provider connections

## Manual Replay Procedure

1. Query failed job IDs for workspace
2. Validate post still eligible for publish
3. Enqueue retry job with new job ID
4. Record operator action in audit log

## Communication Template

- Start time
- Impact scope
- Current mitigation
- Next update ETA
- Resolution summary
