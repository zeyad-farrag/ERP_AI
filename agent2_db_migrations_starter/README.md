# Agent 2 — Data Modeling & Migrations (Laravel 12 / PHP 8.3 / MySQL)

**Mission:** Convert contracts from Agent 1 (`specs/<context>/openapi.json` + `/schemas/*.json`) and DB YAMLs into:
- `database/migrations/*_create_<table>_table.php` (with FKs/indexes)
- `database/seeders/*Seeder.php` (synthetic data from volumes/constraints)
- `app/Models/*.php` (casts, `$fillable`, relationships)
- `specs/db.summary.json` (coverage + drift report)

**Zero‑touch guardrails**
- Exact match to YAML + JSON Schemas (no invented columns).
- 100% FK + index coverage.
- Eloquent relationships from `database_relationships.yml`.
- A **db‑guard** script fails the PR if any drift or missing coverage is detected.

> Inputs (read‑only):  
> `shipping_suite_documentation/database/database_schema_complete.yml`  
> `shipping_suite_documentation/database/database_relationships.yml`  
> `shipping_suite_documentation/database/database_indexes.yml`  
> `specs/<context>/schemas/*.json` (from Agent 1)

> Outputs (write): migrations, models, seeders, `specs/db.summary.json`
