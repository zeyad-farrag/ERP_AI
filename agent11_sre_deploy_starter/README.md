# Agent 11 — SRE / Deploy & Infra

**Mission:** Provide fully automated deploys with canary + bake + auto-promote/rollback, backups/restores, and health checks.
Emit a single machine‑readable verdict to block/allow releases autonomously.

**Inputs (read‑only)**
- `.factory-policy.yml` (canary %, bake time, rollback thresholds)
- App repo (Dockerfile/Procfile, Laravel configs)
- Preview/Prod environment endpoints

**Outputs (write)**
- `.ops/deploy.sh` — build & deploy
- `.ops/canary.sh` — 10% canary, traffic split
- `.ops/rollback.sh` — safe rollback to last green
- `.ops/backup.sh` / `.ops/restore.sh` — DB + app backups & drills
- `.ops/healthcheck.sh` — readiness/liveness probes
- `specs/sre.summary.json` — machine verdict for CI
- `specs/sre.runbook.md` — human-friendly incident/runbook notes

**What is enforced**
- Canary at 10% (from policy), bake for 30m, auto‑promote if SLO deltas hold
- Auto‑rollback on error/latency deltas, SLO breach, or health check failures
- Nightly **backup + restore drill** successful (at least dry‑run in CI)
- Observability: correlation-id, traces, dashboards exist
