from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.users.urls")),
    path("api/", include("apps.businesses.urls")),
    path("api/", include("apps.appointments.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
]
