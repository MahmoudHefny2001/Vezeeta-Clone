from .serializers import ReviewSerializer
from .models import Review
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status, serializers
from django.shortcuts import get_object_or_404
from patient.models import PatientExtended
from doctor.models import DoctorProfile


class ReadReviewtView(generics.RetrieveAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]


class CreateReviewView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]


class RetrieveUpdateDeleteReviewtView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated]


# List reviews view
class ReviewListView(viewsets.ReadOnlyModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (AllowAny,)

    def list(self, request, *args, **kwargs):
        queryset = Review.objects.all()
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = Review.objects.filter(id=kwargs.get("pk"))
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)
