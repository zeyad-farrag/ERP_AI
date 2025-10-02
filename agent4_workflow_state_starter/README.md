# Agent 4 — Workflow & State Machine (Laravel 12)

Mission: Implement approvals and multi‑step workflows exactly as defined in Phase‑0 with idempotency, retries, timeouts and compensations.

Inputs (read‑only)
- shipping_suite_documentation/business_logic/approval_workflows.yml
- specs/<context>/events.yml
- specs/<context>/openapi.json
- specs/<context>/schemas/*.json

Outputs (write)
- app/Workflow/<Context>/*StateMachine.php
- app/Jobs/<Context>/*Job.php
- app/Actions/<Context>/*Action.php
- app/Events/* + app/Listeners/*
- tests/Workflow/*
- specs/workflow.summary.json
