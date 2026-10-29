# Architecture Overview

BookIt is a modular monolith: one Django deployment and one PostgreSQL database, organized into cohesive domain applications rather than independently deployed services.

- `users` owns user identity and roles.
- `businesses` owns businesses and their services.
- `appointments` owns booking and appointment-query behavior.
- `core` owns project configuration, middleware, and narrowly shared cross-cutting code.

Views and serializers are HTTP-boundary adapters. DRF serializers validate requests and serialize responses; domain services hold business behavior and use the Django ORM. Database writes that form one business action are transactional.

Views only route HTTP requests to services and translate HTTP concerns. Services own application behavior and database orchestration. The required database access uses Django ORM; if a future case genuinely requires raw SQL, the named, parameterized query is stored under `sql/` and invoked outside views.

Business Owners manage the businesses and services they own. Clients create appointments and may cancel their own future appointments; Business Owners confirm or cancel appointments for their own businesses. Confirmation applies atomically: it cancels conflicting pending appointments or fails with `409 Conflict` when another conflicting appointment is already confirmed.

Availability-changing operations run inside a database transaction and serialize on the relevant Service row. This prevents concurrent appointment creation or confirmation from producing overlapping confirmed appointments.
