# Disaster Recovery and Backup Plan

## Recovery Objectives

- RPO: 15 minutes
- RTO: 60 minutes

## Backup Strategy

### MongoDB

- Continuous backup or hourly snapshots
- Daily restore validation in staging

### Redis

- AOF persistence enabled
- Snapshot policy depending on provider

### Object Storage (R2)

- Versioning enabled on bucket
- Lifecycle policy for retention

## DR Scenarios

1. API deployment corruption
2. Worker queue processing outage
3. Mongo data loss
4. Redis data corruption

## Recovery Steps (Generic)

1. Freeze writes if required
2. Restore data source from latest valid backup
3. Redeploy known-good application version
4. Run data consistency checks
5. Resume traffic in controlled ramp

## Post-Recovery Validation

- Auth login and refresh flow
- Post create and schedule flow
- Worker publish success and retry flow
- Dashboard status consistency

## DR Drill Cadence

- Run quarterly tabletop simulation
- Run half-yearly restore drill in staging
- Update runbook after each drill
