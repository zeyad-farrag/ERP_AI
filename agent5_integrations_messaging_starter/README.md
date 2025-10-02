# Agent 5 — Integrations & Messaging (Laravel 12 / PHP 8.3)

**Mission:** Implement and verify external connectors and internal messaging with strict safety:
- Payments (PayHub)
- Email/SMS
- Webhooks (signed + replay‑protected)
- Queues (retries, DLQ, parking‑lot)
- Outbox/event publishing

**Inputs (read‑only)**
- `shipping_suite_documentation/integrations/integration_specifications.yml`
- `shipping_suite_documentation/integrations/payhub_integration.yml`
- `specs/<context>/events.yml`
- `specs/<context>/openapi.json` (for inbound/outbound contract shapes)
- `shipping_suite_documentation/business_logic/security_business_rules.yml` (secrets, RBAC constraints)

**Outputs (write)**
- `app/Integrations/PayHub/*` (client, mappers, signature/verification)
- `app/Integrations/EmailSms/*` (drivers, rate‑limits)
- `app/Webhooks/<Vendor>/*` (controllers, signatures, replay windows)
- `app/Messaging/*` (publishers, consumers, outbox)
- `tests/Integrations/*` (Pest, with **contract mocks**)
- `specs/integrations.summary.json` (coverage + sandbox smoke results)

**Non‑negotiables**
- **No secrets in code**; use env/secret manager.
- **Contract mocks** for every external dependency; live **sandbox smoke** gated by a flag.
- **Signature verification** and **replay protection** for inbound webhooks.
- **Retry/backoff** + **DLQ** + **parking‑lot** for outbound failures.
- **Event outbox** to ensure at‑least‑once publish with idempotency headers.
