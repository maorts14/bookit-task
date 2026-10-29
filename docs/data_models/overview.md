# Conceptual Model

A Business Owner owns Businesses. A Business offers Services. A Client creates Appointments for Services.

Appointment start times are accepted as ISO 8601 timestamps with an offset and normalized to UTC for storage and querying. A new appointment begins in `Pending`; a Business Owner may confirm or cancel it, and its Client may cancel it.
