from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.ClinicViewSet.as_view()),
]
