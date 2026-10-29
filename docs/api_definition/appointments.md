# Appointment Listing

`GET /api/appointments` returns only appointments visible to the authenticated caller: a Client sees their own appointments, and a Business Owner sees appointments for services offered by businesses they own.

The result uses `page` and `page_size` pagination, with a default page size of `20`, a maximum of `100`, and `count`, `next`, `previous`, and `results` response fields.

The endpoint supports the assignment-required optional `from`, `to`, and `status` filters. Their detailed semantics are defined separately as the API contract is finalized.
