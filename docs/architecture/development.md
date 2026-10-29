# Development Environment

`docker compose --profile dev up --build` starts the local PostgreSQL database and API development stack.

In the development profile, the API waits for PostgreSQL, applies migrations, runs the idempotent `seed_data` management command, and then starts the Django development server. Demo data is never seeded by a production configuration.
