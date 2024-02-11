from .serializers import ReviewSerializer
from .models import Review
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status, serializers
from django.shortcuts import get_object_or_404
from patient.models import PatientExtended
from doctor.models import DoctorProfile




class ReviwModelViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = Review.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(PatientExtended, user=request.user)
            doctor = get_object_or_404(DoctorProfile, id=request.data["doctor"])
            review = Review.objects.create(
                comment=request.data["comment"], rate=request.data["rate"], user=user, doctor=doctor
            )
            review.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get_queryset(self):
        queryset = Review.objects.all()
        doctor = self.request.query_params.get('doctor', None)
        if doctor is not None:
            queryset = queryset.filter(doctor=doctor)
        return queryset


# class ReadReviewtView(generics.RetrieveAPIView):
#     serializer_class = ReviewSerializer
#     permission_classes = [IsAuthenticated]


# class CreateReviewView(generics.CreateAPIView):
#     serializer_class = ReviewSerializer
#     permission_classes = [IsAuthenticated]


# class RetrieveUpdateDeleteReviewtView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     lookup_field = "id"
#     permission_classes = [IsAuthenticated]


# # List reviews view
# class ReviewListView(viewsets.ReadOnlyModelViewSet):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     permission_classes = (AllowAny,)

#     def list(self, request, *args, **kwargs):
#         queryset = Review.objects.all()
#         serializer = ReviewSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, *args, **kwargs):
#         queryset = Review.objects.filter(id=kwargs.get("pk"))
#         serializer = ReviewSerializer(queryset, many=True)
#         return Response(serializer.data)
