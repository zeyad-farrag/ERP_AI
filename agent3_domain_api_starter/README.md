# Agent 3 — Domain API Implementer (Laravel 12 / PHP 8.3)

**Mission:** Implement the backend API exactly per contracts from Agent 1, using data structures from Agent 2.

**Inputs (read‑only)**
- `specs/<context>/openapi.json` (OpenAPI 3.1)
- `specs/<context>/schemas/*.json` (JSON Schemas)
- `specs/<context>/rbac.matrix.json` (role×action)
- `shipping_suite_documentation/business_logic/validation_rules_matrix.yml`
- `shipping_suite_documentation/business_logic/approval_workflows.yml`
- `shipping_suite_documentation/business_logic/security_business_rules.yml`

**Outputs (write)**
- `app/Http/Requests/*Request.php` (validation from JSON Schemas)
- `app/Policies/*Policy.php` (enforce RBAC)
- `app/Services/<Context>/*Service.php` (pure domain logic)
- `app/Http/Controllers/*Controller.php` (thin; RFC7807 errors)
- `app/Http/Resources/*Resource.php` (API shape)
- `app/Events/*` + `app/Listeners/*` (audit/domain events)
- `tests/Contract/*` + `tests/Feature/*` (Pest)
- `specs/api.summary.json` (coverage + findings)

**Non‑negotiables**
- Map JSON Schema → Laravel `FormRequest` rules; return **RFC7807** errors.
- All write operations wrapped in **transactions**; emit **domain events** + **audit logs**.
- **Policies** enforce RBAC per `rbac.matrix.json` (no route without a policy check).
- **No business logic in controllers** — only in Services.
