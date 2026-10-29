# Tests

Run the full isolated PostgreSQL suite with `docker compose --profile test run --rm test`.

The test profile uses a separate `test-db` server and Django creates a fresh test database for the run; it does not use the development database or its demo data.

- `appointments/` tests booking, confirmation, conflicts, and cancellation capacity release.
- `api/` tests the public HTTP contract, authentication, authorization, response privacy, summaries, and middleware behavior.
