# Agent 9 — Compliance & Audit (Laravel 12 / PHP 8.3)

**Mission:** Enforce data retention, export controls, auditability, and provenance across the ERP.
Emit a single machine‑readable verdict to block/allow merges autonomously.

**Inputs (read‑only)**
- `shipping_suite_documentation/security/security_business_rules.yml`
- `shipping_suite_documentation/governance/*` (retention/export policies if present)
- `specs/<context>/openapi.json`, `specs/<context>/events.yml`
- Source code for audit logging & exports

**Outputs (write)**
- `specs/compliance.summary.json`
- If needed, generated cron/queue jobs for retention (`app/Console/Commands/*`, `app/Jobs/*`)
- Export provenance hooks and loggers

**What is enforced**
- Retention jobs exist & are scheduled for regulated entities (clients, staff, invoices, payments, communications)
- Exports log requester identity, purpose, timestamp, and include a provenance stamp
- Money flows are **auditable end‑to‑end** (payments/refunds/ledger entries/approvals)
- Audit trail writes on sensitive operations with correlation id and actor ip
- No PII is exported without explicit purpose; redaction rules apply
