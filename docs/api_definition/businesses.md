# Business Discovery

`GET /api/businesses` returns authenticated, paginated business discovery results.

- It accepts `page` and `page_size`; page size defaults to `20` and is capped at `100`.
- Its response has `count`, `next`, `previous`, and `results` fields.
- `category` is a case-insensitive exact category filter.
- `search` is a case-insensitive partial match against the business name.
- Supplying both filters applies both conditions.
