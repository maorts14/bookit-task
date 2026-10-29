# Business Discovery

`GET /api/businesses` returns authenticated, paginated business discovery results.

- It accepts `page` and `page_size`; page size defaults to `20` and is capped at `100`.
- Its response has `count`, `next`, `previous`, and `results` fields.
- `category` is a case-insensitive exact category filter.
- `search` is a case-insensitive partial match against the business name.
- Supplying both filters applies both conditions.
- Results are ordered newest first by `created_at`, then by descending `id` as a tie-breaker.
- Business and Service read responses include `created_at` and `updated_at`.

`GET /api/businesses/{id}` is available to every authenticated user and includes that business's services. Business Owners use `PATCH` to partially update owned businesses or services; successful updates return the updated resource with `200 OK`. Successful hard deletes return `204 No Content`.
