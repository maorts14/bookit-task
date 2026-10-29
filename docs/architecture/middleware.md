# Middleware

## Global exception handling

Unhandled exceptions produce a generic Problem Details-style JSON response with status `500`. Client responses contain no exception message, traceback, or internal detail; the full exception is logged server-side.

## Request logging

Every response includes `X-Correlation-ID`. The middleware reuses a non-empty incoming value or generates a UUID when absent. Request logs include method, path, response status, duration, and correlation ID; they never include request bodies, passwords, JWTs, or authorization headers.
