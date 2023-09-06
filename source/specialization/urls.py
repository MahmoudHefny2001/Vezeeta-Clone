from django.urls import path, include
from .import views


urlpatterns = [
    path("available/", views.SpecializationListView.as_view(), name="specialization_list"),
]

