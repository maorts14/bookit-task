from django.http import HttpResponse
from django.urls import path


def explode(_request):
    raise RuntimeError("secret stack detail")


urlpatterns = [path("explode", explode)]
