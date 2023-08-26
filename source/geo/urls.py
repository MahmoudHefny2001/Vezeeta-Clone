from django.urls import path, include
from .views import (
    AddressViewSet,
    CitiesListView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"", AddressViewSet)


urlpatterns = [
    path('cities/', CitiesListView.as_view(), name='cities-list'),
    path("", include(router.urls)),
]