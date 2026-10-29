from django.urls import path

from .views import BusinessDetailView, BusinessListCreateView, BusinessSummaryView, ServiceCreateView, ServiceDetailView


urlpatterns = [
    path("businesses", BusinessListCreateView.as_view(), name="business-list"),
    path("businesses/<uuid:business_id>", BusinessDetailView.as_view(), name="business-detail"),
    path("businesses/<uuid:business_id>/summary", BusinessSummaryView.as_view(), name="business-summary"),
    path("businesses/<uuid:business_id>/services", ServiceCreateView.as_view(), name="service-create"),
    path("services/<uuid:service_id>", ServiceDetailView.as_view(), name="service-detail"),
]
