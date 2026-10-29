# Development Environment

`docker compose --profile dev up --build` starts the local PostgreSQL database and API development stack.

In the development profile, the API waits for PostgreSQL, applies migrations, runs the idempotent `seed_data` management command, and then starts the Django development server. Demo data is never seeded by a production configuration.

The development profile mounts the source code into the API container and uses Django auto-reload. If Docker Desktop file events prove unreliable, polling is an opt-in documented setting.

The seed command creates 5 Business Owners, 10 Clients, 20 Businesses, 50 Services, and 200 Appointments. It includes past and future appointments around its initial seed time, all appointment statuses, and overlapping pending requests for lifecycle demonstrations.

An internal, unexposed `DemoSeedMarker` record with key `demo-seed-v1` stores the initial seed-time anchor. It is created in the same transaction as the fixture dataset. When the marker already exists, seeding is skipped; on failure, the marker and all fixture writes roll back together.

The README documents development-only credentials for every seeded account: `owner1@bookit.local` through `owner5@bookit.local`, and `client1@bookit.local` through `client10@bookit.local`. All use `BookItDemo123!`.
