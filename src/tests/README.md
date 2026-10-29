# Tests

Run the full isolated PostgreSQL suite with:

```bash
docker compose -f docker-compose.test.yml up --build --abort-on-container-exit --exit-code-from test
docker compose -f docker-compose.test.yml down -v
```

The test stack uses a separate `test-db` server and Django creates a fresh test database for the run; it does not use the development database or its demo data.

- `appointments/` tests booking, confirmation, conflicts, cancellation capacity release, and seed idempotency.
- `api/` tests the public HTTP contract, authentication validation, business/service management, authorization, response privacy, summaries, filters, and middleware behavior.
