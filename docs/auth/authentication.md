# Authentication

Registration is public. A registrant selects either the `Client` or `BusinessOwner` role; BookIt v1 has no administrative or staff role.

Login returns one JWT access token containing at least the user's ID and role. The token has a fixed expiry, and v1 does not provide refresh tokens or a refresh endpoint.
