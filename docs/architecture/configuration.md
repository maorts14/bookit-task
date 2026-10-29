# Configuration and Database Scope

Runtime configuration is provided through environment variables. `.env.example` documents required local values; `.env` is ignored by Git and contains development-only values. No real secret is committed.

The development Compose profile exposes the API on port `8000` and PostgreSQL on port `5432`.

Django uses autocommit with `CONN_MAX_AGE=0`, so database connections are scoped to individual requests. Explicit `transaction.atomic()` blocks protect multi-write appointment and seed operations.
