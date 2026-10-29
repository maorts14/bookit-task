from rest_framework.exceptions import APIException


class AvailabilityConflict(APIException):
    status_code = 409
    default_detail = "The requested service is unavailable for this time window."
    default_code = "availability_conflict"


class ServiceTemporarilyLocked(APIException):
    status_code = 423
    default_detail = "The requested service is temporarily locked while another booking is being processed. Your request was not processed; retry shortly."
    default_code = "service_temporarily_locked"
