# Testing Strategy

BookIt uses a feature-based pytest suite.

- Appointment service unit tests cover booking validation, confirmation, conflict handling, cancellation, and capacity release.
- API integration tests cover authentication, role ownership, CRUD behavior, pagination, filtering, and documented errors.
- Middleware tests cover generic internal-error responses, correlation IDs, and safe request logging.
- Seed tests cover expected volumes, lifecycle-data coverage, and idempotent re-runs.
- Concurrency tests cover competing availability-changing requests and the locked-service response.
