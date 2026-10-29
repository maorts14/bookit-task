# Postman Collection

The collection is derived from `docs/api_definition/openapi.yaml`. It adds runnable requests, examples, and assertions that OpenAPI alone does not express.

For every API change, update the OpenAPI contract first and then update the affected collection requests and assertions in the same commit.

The collection uses `baseUrl`, `bearerToken`, `client_token`, and `owner_token` variables. Run the dedicated owner or client login request to populate the matching token and active `bearerToken` before executing protected requests.
# Using the collection in Postman Desktop

For Postman Desktop, import these two files rather than opening the YAML source folder as a workspace:

- `postman/imports/BookIt API.postman_collection.json`
- `postman/imports/BookIt Local.postman_environment.json`

Select the **BookIt Local** environment and run **Auth / Login owner** or
**Auth / Login client** before protected requests. The YAML source collection
remains the Git-friendly source of truth. To refresh the import files after a
source change, run `python scripts/export_postman_imports.py`.

