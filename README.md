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
src/config/             Django settings and root routing
src/core/               Middleware and cross-cutting code
src/apps/users/         Custom user model and authentication
src/apps/businesses/    Businesses, services, and aggregate summary
src/apps/appointments/  Booking, availability, and appointment lifecycle
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

The development Compose stack uses `POSTGRES_HOST=db`. Do not commit real secrets.

## Run the development API

Start the complete development stack:

```bash
docker compose up --build
```

The API is available at `http://localhost:8000`. Startup waits for PostgreSQL, runs migrations, creates the demo dataset once, and starts Django auto-reload. Stop it with `docker compose down`.

To remove development database data deliberately:

```bash
docker compose down -v
```

## Run tests in an isolated environment

Tests use a separate Compose file and a separate PostgreSQL container; they never touch development data:

```bash
docker compose -f docker-compose.test.yml up --build --abort-on-container-exit --exit-code-from test
docker compose -f docker-compose.test.yml down -v
```

The first command returns Pytest's exit code. The second command removes the stopped test containers and their database storage. Pytest creates a fresh Django test database for every run and does not use the development database, its volume, or demo records.

For a focused feature suite:

```bash
docker compose -f docker-compose.test.yml run --rm test pytest tests/appointments
docker compose -f docker-compose.test.yml down -v
```

## Seeded demo credentials

All demo accounts use the development-only password `BookItDemo123!`.

| Role | Email | Password |
| --- | --- | --- |
| Business Owner | `owner1@bookit.local` | `BookItDemo123!` |
| Business Owner | `owner2@bookit.local` | `BookItDemo123!` |
| Business Owner | `owner3@bookit.local` | `BookItDemo123!` |
| Business Owner | `owner4@bookit.local` | `BookItDemo123!` |
| Business Owner | `owner5@bookit.local` | `BookItDemo123!` |
| Client | `client1@bookit.local` | `BookItDemo123!` |
| Client | `client2@bookit.local` | `BookItDemo123!` |
| Client | `client3@bookit.local` | `BookItDemo123!` |
| Client | `client4@bookit.local` | `BookItDemo123!` |
| Client | `client5@bookit.local` | `BookItDemo123!` |
| Client | `client6@bookit.local` | `BookItDemo123!` |
| Client | `client7@bookit.local` | `BookItDemo123!` |
| Client | `client8@bookit.local` | `BookItDemo123!` |
| Client | `client9@bookit.local` | `BookItDemo123!` |
| Client | `client10@bookit.local` | `BookItDemo123!` |

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
