# Business Summary

`GET /api/businesses/{id}/summary` is available only to the owning Business Owner. For each service of that business, it returns the number of future, non-cancelled appointments and the corresponding expected revenue, calculated as appointment count multiplied by service price.

The calculation is performed with Django ORM aggregation in the database. Expected revenue is represented as an exact decimal string in the API response.
