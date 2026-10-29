from django.urls import path

from .views import AppointmentListCreateView, AppointmentStatusView


urlpatterns = [
    path("appointments", AppointmentListCreateView.as_view(), name="appointment-list"),
    path("appointments/<uuid:appointment_id>/status", AppointmentStatusView.as_view(), name="appointment-status"),
]
