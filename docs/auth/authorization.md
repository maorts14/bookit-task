# Authorization

All API endpoints except registration and login require authentication.

- A Client may create appointments and cancel only their own future, non-cancelled appointments.
- A Business Owner may create, edit, and delete only businesses and services they own.
- A Business Owner may confirm or cancel only appointments for services offered by businesses they own. Confirming an appointment conflicts with no existing confirmed appointment for that service's time window; otherwise the operation fails with `409 Conflict` and makes no changes.
