# Conceptual Model

A Business Owner owns Businesses. A Business offers Services. A Client creates Appointments for Services.

Appointment start times are accepted as ISO 8601 timestamps with an offset and normalized to UTC for storage and querying. A new appointment begins in `Pending`; a Business Owner may confirm or cancel it, and its Client may cancel it.

Each Service represents one worker-specific capacity in v1. Pending Appointments may overlap. A confirmed Appointment occupies its Service for its duration: conflicting pending appointments are cancelled when one is confirmed, and a Client cannot create an Appointment that conflicts with a confirmed Appointment.
