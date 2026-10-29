# Configuration and Database Scope

Runtime configuration is provided through environment variables. `.env.example` documents required local values; `.env` is ignored by Git and contains development-only values. No real secret is committed.

`docker-compose.yml` is the development stack and exposes the API on port `8000` and PostgreSQL on port `5432`.
`docker-compose.test.yml` is a separate, unexposed test-only stack with its own PostgreSQL service and no development
database volume.

Django uses autocommit with `CONN_MAX_AGE=0`, so database connections are scoped to individual requests. Explicit `transaction.atomic()` blocks protect multi-write appointment and seed operations.
