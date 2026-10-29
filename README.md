# BookIt Task

BookIt is an appointment-booking API for business owners and clients, built with Python 3.12, Django 5, Django REST Framework, PostgreSQL, and JWT authentication.

## What it supports

- Client and Business Owner registration plus 60-minute JWT access tokens.
- Authenticated business discovery with filters, pagination, and details.
- Owner CRUD for businesses and worker-specific services.
- Client appointment requests, owner confirmation/cancellation, and client cancellation.
- Per-service booking capacity based on time-window overlap.
- Owner-only ORM business summaries, safe request logging, correlation IDs, and generic internal-error handling.

## Project layout

```text
config/                 Django settings and root routing
core/                   Middleware and cross-cutting code
apps/users/             Custom user model and authentication
apps/businesses/        Businesses, services, and aggregate summary
apps/appointments/      Booking, availability, and appointment lifecycle
docs/                   Design records, API notes, and domain language
postman/                One importable Postman collection
tests/                  Feature-organized pytest suite
sql/                    Reserved for future named raw SQL queries
```

## Prerequisites

- Docker Desktop with the Linux container engine running.
- Or Python 3.12 plus PostgreSQL 16 if running the application outside Compose.

## Configuration

`.env` is a local development file and is ignored by Git. It is already included for this workspace. For another clone, copy `.env.example` to `.env` and set a local `DJANGO_SECRET_KEY`.

The development Compose profile uses `POSTGRES_HOST=db`. Do not commit real secrets.

## Run the development API

Start the complete development stack:

```bash
docker compose --profile dev up --build
```

The API is available at `http://localhost:8000`. Startup waits for PostgreSQL, runs migrations, creates the demo dataset once, and starts Django auto-reload. Stop it with `docker compose --profile dev down`.

To remove development database data deliberately:

```bash
docker compose --profile dev down -v
```

## Run tests in an isolated environment

Run tests only through the dedicated test profile:

```bash
docker compose --profile test run --rm test
```

This starts a separate `test-db` PostgreSQL server. Pytest creates a fresh Django test database for every run and does not use the development database, its volume, or demo records.

For a focused feature suite:

```bash
docker compose --profile test run --rm test pytest tests/appointments
```

## Seeded demo credentials

All demo accounts use the development-only password `BookItDemo123!`.

| Role | Emails |
| --- | --- |
| Business Owner | `owner1@bookit.local` through `owner5@bookit.local` |
| Client | `client1@bookit.local` through `client10@bookit.local` |

The one-time idempotent seed produces 5 Business Owners, 10 Clients, 20 Businesses, 50 Services, and 200 Appointments distributed a few days before and after the first seed time.

## API and Postman

The OpenAPI contract is at [`docs/api_definition/openapi.yaml`](docs/api_definition/openapi.yaml). Import [`postman/BookIt API.postman_collection.json`](postman/BookIt%20API.postman_collection.json) into Postman Desktop. It defaults to `http://localhost:8000` and captures the demo owner/client access tokens after login.

## Database connections and transactions

Django runs with autocommit and `CONN_MAX_AGE=0`, so database connections are scoped to individual requests. Appointment creation, confirmation, cancellation, and seed creation use explicit `transaction.atomic()` blocks; availability-changing operations lock the relevant Service row so conflicting confirmations cannot both succeed.

## Design documentation

- [`docs/context.md`](docs/context.md) contains the domain vocabulary.
- [`docs/architecture/`](docs/architecture/) contains decisions and operational design.
- [`docs/data_models/`](docs/data_models/) explains the conceptual model.
- [`docs/api_definition/`](docs/api_definition/) contains contract notes and the OpenAPI specification.
