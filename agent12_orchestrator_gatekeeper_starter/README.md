# Agent 12 — Orchestrator & Policy Gatekeeper

**Mission:** Read `.factory-policy.yml`, run/sequence agents, and **gate** merges & deploys based on machine verdicts only
(ZERO human approvals). If anything violates policy, block or auto‑rollback.

**Consumes (read‑only verdicts)**
- `specs/summary.report.json`                # Agent 1 (Spec Authority)
- `specs/db.summary.json`                    # Agent 2
- `specs/api.summary.json`                   # Agent 3
- `specs/workflow.summary.json`              # Agent 4
- `specs/integrations.summary.json`          # Agent 5
- `specs/ui.summary.json`                    # Agent 6
- `specs/qa.summary.json`                    # Agent 7
- `specs/security.summary.json`              # Agent 8
- `specs/compliance.summary.json`            # Agent 9
- `specs/perf.summary.json`                  # Agent 10
- `specs/sre.summary.json`                   # Agent 11

**Produces (write)**
- `specs/factory.decision.json`  — final pass/fail + reasons
- (Optionally) merges PRs, tags releases, and posts notifications based on decision.

The Orchestrator DOES NOT re‑evaluate the app logic. It only enforces policy across each agent’s **machine verdict**.
