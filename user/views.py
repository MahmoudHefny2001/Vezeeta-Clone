from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .authentication import CustomUserAuthBackend
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, ProfileSerializer
from rest_framework import status, generics, mixins, viewsets
from django.conf import settings
import jwt
from .models import CustomUser, Profile


class SignUpView(APIView):
    permission_classes = []
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)



class LoginView(APIView):
    permission_classes = []
    def post(self, request):
        email_or_phone = request.data.get('email_or_phone')
        password = request.data.get('password')
        user = CustomUserAuthBackend().authenticate(request=request, username=email_or_phone, password=password)

        if user is not None:
            access_token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)
            return Response({
                'access': str(access_token),

                'refresh': str(refresh_token),
            })
        else:
            return Response({
                'error': 'Invalid credentials',
            }, status=status.HTTP_401_UNAUTHORIZED)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Profile.objects.all()
        else:
            return Profile.objects.filter(user=user)
    