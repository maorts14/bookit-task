# API Tests

Run this feature area with:

```bash
docker compose -f docker-compose.test.yml run --rm test pytest src/tests/api
docker compose -f docker-compose.test.yml down -v
```

- `test_api_contract.py` covers auth responses, appointment ownership, and documented error statuses.
- `test_authentication_edges.py` covers duplicate emails, weak passwords, invalid credentials, and JWT claims.
- `test_business_management.py` covers discovery, ownership-protected CRUD, validation, and delete cascades.
- `test_appointment_contract.py` covers list filters, role-scoped results, booking validation, and state transitions.
- `test_summary_and_errors.py` covers ORM summary values and middleware behavior.
