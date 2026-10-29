# Appointment Listing

`GET /api/appointments` returns only appointments visible to the authenticated caller: a Client sees their own appointments, and a Business Owner sees appointments for services offered by businesses they own.

The result uses `page` and `page_size` pagination, with a default page size of `20`, a maximum of `100`, and `count`, `next`, `previous`, and `results` response fields.

The endpoint supports the assignment-required optional `from`, `to`, and `status` filters. `from` is inclusive and `to` is exclusive; they compare against `start_time`. `status` accepts one exact appointment status per request. Invalid filter values return `400 Bad Request`.

Results are ordered by ascending `start_time`, then ascending `id` as a tie-breaker.

If another request currently holds the availability lock for the requested service, the operation returns `423 Locked` with code `service_temporarily_locked` and a message stating that the requested service is temporarily locked, the request was not processed, and the caller should retry shortly.
