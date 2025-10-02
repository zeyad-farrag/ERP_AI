# Agent 6 — UI/UX Generator (Laravel Blade + Livewire)

**Mission:** Generate consistent UI for each OpenAPI resource:
- CRUD pages (index/table, create, edit, show)
- Forms with client hints derived from JSON Schemas
- RBAC-aware controls (hide/disable actions user cannot perform)
- Playwright E2E + visual snapshot tests

**Inputs (read‑only)**
- `specs/<context>/openapi.json`
- `specs/<context>/schemas/*.json`
- `specs/<context>/rbac.matrix.json`

**Outputs (write)**
- `resources/views/<context>/*.blade.php`
- `app/Livewire/<Context>/*Component.php`
- `resources/views/components/ui/*` (reusable widgets)
- `tests/E2E/<Context>/*.spec.ts` (Playwright)
- `playwright.config.ts` + snapshot baseline directory
- `specs/ui.summary.json` (coverage + findings)

**Non‑negotiables**
- Client‑side hints (required, min/max, patterns) mirror JSON Schemas.
- RBAC is enforced **in UI** (no visible buttons/links for forbidden actions).
- Tables include sort/filter/pagination.
- Forms show server validation errors (RFC7807) cleanly.
