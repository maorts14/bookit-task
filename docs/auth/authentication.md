# Authentication

Registration is public. A registrant selects either the `Client` or `BusinessOwner` role; BookIt v1 has no administrative or staff role.

Email is normalized to lowercase and unique without regard to case. Registration uses Django's built-in password validators.

Login returns one JWT access token containing at least the user's ID and role. Invalid email and password combinations both return the same generic `401` response and do not disclose whether an account exists. The token has a fixed expiry, and v1 does not provide refresh tokens or a refresh endpoint.
