# Business and service deletion cascades to appointments

BookIt v1 uses hard deletion for owner-managed businesses and services. Deleting a Service removes its appointments, and deleting a Business removes its services and their appointments, even when future confirmed appointments exist; Users are outside this cascade. This deliberately favors complete owner-controlled removal over preserving client appointment history.
