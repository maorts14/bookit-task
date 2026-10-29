# Appointment Tests

Run this feature area with:

```bash
docker compose -f docker-compose.test.yml run --rm test pytest src/tests/appointments
docker compose -f docker-compose.test.yml down -v
```

The tests exercise service-layer rules without HTTP and use the isolated test database.
