# Architecture Overview

BookIt is a modular monolith: one Django deployment and one PostgreSQL database, organized into cohesive domain applications rather than independently deployed services.

- `users` owns user identity and roles.
- `businesses` owns businesses and their services.
- `appointments` owns booking and appointment-query behavior.
- `core` owns project configuration, middleware, and narrowly shared cross-cutting code.

Views and serializers are HTTP-boundary adapters. Domain services hold business behavior and use the Django ORM; database writes that form one business action are transactional.
