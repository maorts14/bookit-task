# Postman Collection

The collection is derived from `docs/api_definition/openapi.yaml`. It adds runnable requests, examples, and assertions that OpenAPI alone does not express.

For every API change, update the OpenAPI contract first and then update the affected collection requests and assertions in the same commit.

The collection uses `base_url`, client-token, and owner-token variables. It authenticates its demo users and asserts successful responses plus validation, `401`, `403`, `404`, `409`, and `423` error paths.
