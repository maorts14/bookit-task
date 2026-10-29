# BookIt Appointment Booking

BookIt is the appointment-booking domain in which business owners offer services and clients reserve appointments for those services.

## Language

**Client**:
A user who books an appointment for a service.
_Avoid_: Customer, consumer

**Business Owner**:
A user who owns one or more businesses, manages their services, and manages appointments for those businesses.
_Avoid_: Provider, merchant

**Business**:
An owner-operated listing that offers one or more services.
_Avoid_: Provider, venue

**Service**:
A bookable offering belonging to one business, defined by a duration and price.
_Avoid_: Offering, treatment

**Appointment**:
A client's request for one service at a start time, with a lifecycle status managed by the client and the relevant business owner.
_Avoid_: Booking, reservation

**Appointment Status**:
The lifecycle state of an appointment: `Pending`, `Confirmed`, or `Cancelled`.
_Avoid_: Booking status
