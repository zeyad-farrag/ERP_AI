# Agent 10 — Performance & Cost (Laravel 12 / MySQL)

**Mission:** Enforce latency/error budgets, detect N+1/unbounded queries, propose indexes & caching, and watch LLM/external costs.
Emit a single machine‑readable verdict to block/allow merges autonomously.

**Inputs (read‑only)**
- `specs/<context>/openapi.json`
- `shipping_suite_documentation/database/database_indexes.yml`
- App source & tests; preview URL for synthetic load

**Outputs (write)**
- `specs/perf.summary.json`
- k6/Locust scripts under `tools/perf/`
- Index & cache hints under `specs/perf.hints.json`

**What is enforced**
- p95 latency budgets: reads ≤ 350ms, writes ≤ 500ms
- Error rate ≤ 1.0%
- Detect and fail on N+1 or unbounded queries (missing LIMIT/pagination, cartesian joins)
- Propose concrete indexes (table, columns, type) when budgets fail
- Cost guardrails (optional): report top endpoints by external/LLM calls
