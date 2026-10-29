# Development Environment

`docker compose --profile dev up --build` starts the local PostgreSQL database and API development stack.

In the development profile, the API waits for PostgreSQL, applies migrations, runs the idempotent `seed_data` management command, and then starts the Django development server. Demo data is never seeded by a production configuration.

The seed command creates 5 Business Owners, 10 Clients, 20 Businesses, 50 Services, and 200 Appointments. It uses `get_or_create` for deterministic fixture records; an appointment is identified by its Service, Client, and start time, so repeated development startups do not duplicate seed data.
