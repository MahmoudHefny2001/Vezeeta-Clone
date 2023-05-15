from django.shortcuts import render
from .models import Doctor
from .serializers import DoctorSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework import viewsets, generics, mixins, views
from rest_framework.response import Response
from rest_framework import status

class DoctorRegistrationView(views.APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [AllowAny, IsAuthenticatedOrReadOnly]
    # Define the allowed methods for users
    http_method_names = ['get', 'head', 'options']

class DoctorSelfViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    # Define the allowed methods for doctors themselves
    http_method_names = ['get', 'head', 'post', 'put', 'patch', 'delete']