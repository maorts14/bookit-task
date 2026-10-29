# Authentication API

`POST /api/auth/register` accepts `email`, `password`, `full_name`, and `role`. It returns `201 Created` with the new user's non-sensitive fields; clients log in separately to receive an access token.

`POST /api/auth/login` returns an access token in this shape:

```json
{
  "access_token": "<JWT>",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

Ordinary request-validation errors use DRF's standard field-keyed `400 Bad Request` JSON response shape.
