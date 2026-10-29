# Conceptual Model

A Business Owner owns Businesses. A Business offers Services. A Client creates Appointments for Services. Service prices use precise decimal values. User, Business, Service, and Appointment identities are UUIDs.

Every Business has a non-blank free-text category. Every Service has a non-blank name, a strictly positive duration in minutes, and a non-negative price.

Every User, Business, Service, and Appointment has a UTC `created_at` timestamp. These timestamps are set by the system when records are created. Mutable records also have a UTC `updated_at` timestamp maintained whenever they change.

Appointment start times are accepted as ISO 8601 timestamps with an offset and normalized to UTC for storage and querying. A new appointment begins in `Pending`; a Business Owner may confirm or cancel it, and its Client may cancel it.

Each Service represents one worker-specific capacity in v1. Pending Appointments may overlap. A confirmed Appointment occupies its Service for its duration: conflicting pending appointments are cancelled when one is confirmed, and a Client cannot create an Appointment that conflicts with a confirmed Appointment. Cancelling a confirmed Appointment releases that capacity immediately; previously cancelled competing appointments are not revived.

Appointment creation requires a strictly future start time. The only allowed status transitions are `Pending → Confirmed`, `Pending → Cancelled`, and `Confirmed → Cancelled`; `Cancelled` is terminal.

Deleting a Service hard-deletes every Appointment for that Service. Deleting a Business hard-deletes its Services and, through them, their Appointments. Neither operation deletes any User.
