from django.urls import path, include
from .views import SignUpView, LoginView, ProfileViewSet
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'^profiles', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('sign-up/', SignUpView.as_view(), name='user_signup'),
    path('login/', LoginView.as_view(), name='user_signup'),
    
]