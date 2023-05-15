from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'^search', views.UserDoctorViewSet)
router.register(r'^accounts', views.DoctorSelfViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('sign-up/', views.DoctorRegistrationView.as_view(), name='doctor-registration'),
    # path('login/', ),
    # path('logout/', ),
    # path('change-password/', )

]