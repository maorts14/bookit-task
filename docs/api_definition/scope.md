# API Scope

The authoritative operation and schema definitions will live in `openapi.yaml` once endpoint details are finalized.

BookIt v1 includes the assignment-required registration, login, business listing, appointment creation/listing, and owner-only business-summary endpoints. It additionally includes business detail with services, Business Owner CRUD for owned businesses and services, and role-aware appointment status updates.

Clients reschedule by cancelling their existing appointment and creating a new one; v1 has no in-place appointment time or service update.

Business and service deletion is a hard-delete cascade: deleting a service removes all of its appointments; deleting a business removes its services and their appointments. This remains allowed when future confirmed appointments exist, and never deletes User records.

Appointments can only be created for a strictly future time. The status endpoint permits `Pending → Confirmed` for the owning Business Owner, cancellation of pending or confirmed appointments by the Client or owning Business Owner, and no transition from `Cancelled`.
