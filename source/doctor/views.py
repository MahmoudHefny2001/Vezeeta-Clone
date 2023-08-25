from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import (
    Doctor,
    DoctorProfile,
    DoctorExtended,
)
from .serializers import (
    DoctorSerializer,
    DoctorProfileSerializer,
    OuterViewDoctorSerializer,
    OuterViewDoctorProfileSerializer,

)
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    AllowAny,
)
from rest_framework import viewsets, generics, mixins, views, permissions
from rest_framework.response import Response
from rest_framework import status
from person.authentication import CustomUserAuthBackend
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import filters
from review.models import Review
from review.serializers import ReviewSerializer
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.pagination import PageNumberPagination
from .permissions import IsProfileOwner
from django_filters.rest_framework import DjangoFilterBackend 
 
from django.db.models import Q

from rest_framework_word_filter import FullWordSearchFilter


# from .filters import CityFilterBackend


class DoctorListPagination(PageNumberPagination):
    page_size = 10  # Number of results per page
    page_size_query_param = 'page_size'
    max_page_size = 100



class DoctorRegistrationView(views.APIView):
    permission_classes = [AllowAny,]
    
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    

    def post(self, request):
        # try:
        #     serializer = DoctorSerializer(data=request.data)
        #     serializer.is_valid(raise_exception=True)

        #     # Make sure you pass the specialization choice correctly in the data
        #     specialization_choice = request.data.get("specialization")
        #     if specialization_choice not in dict(DoctorExtended.SPECIAIALIZATION_CHOICES):
        #         return Response({"error": "Invalid specialization choice"}, status=status.HTTP_400_BAD_REQUEST)
            
        #     serializer.save(specialization=specialization_choice)  # Save specialization
            
        #     return Response(serializer.data)
        # except Exception as e:
        #     print(e)
        #     raise e
        pass


class LoginView(views.APIView):
    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]


    def post(self, request):
        email_or_phone = request.data.get("email_or_phone")
        password = request.data.get("password")

        try:
        
            doctor = CustomUserAuthBackend().authenticate(
                request=request, username=email_or_phone, password=password
            )


            doctor_profile_id = DoctorProfile.objects.filter(doctor=doctor).first().id
        
            doctor_name = DoctorProfile.objects.filter(doctor=doctor).first().doctor.full_name

            if doctor is not None:
                access_token = AccessToken.for_user(doctor)
                refresh_token = RefreshToken.for_user(doctor)
                return Response(
                    {
                        "access": str(access_token),
                        "refresh": str(refresh_token),

                        "doctor_profile_id": doctor_profile_id,
                        "doctor_name": doctor_name,
                    }
                )
            else:
                return Response(
                    {
                        "error": "Invalid credentials",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        except Exception as e:
            return Response(
                {"error": f" An error occurred: {str(e)} "},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DoctorProfileViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = DoctorListPagination

    queryset = DoctorProfile.objects.all()
    
    permission_classes = [IsAuthenticatedOrReadOnly]

    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter, 
        FullWordSearchFilter,
    ]


    word_fields = (
        'doctor__full_name',
        'doctor__specialization__specialization',
        'doctor__qualifications',
        'doctor__address__name',
        'doctor__address__location__city',
    )

    filterset_fields = [
        'doctor__full_name',
        'doctor__address__name',
        'doctor__address__location__city',
        'doctor__specialization__specialization',
        'doctor__qualifications',    
    ] 

    
    search_fields = [  
        'doctor__specialization__specialization',
        'doctor__address__name',
        'doctor__address__location__city',
        'doctor__full_name',
        'doctor__qualifications',
    ]   


    def get_serializer_class(self):
        if self.action == "list":
            return OuterViewDoctorProfileSerializer
        return DoctorProfileSerializer


    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            # Allow any user to list and retrieve doctors
            return [permissions.AllowAny()]
        else:
            # Only authenticated users can perform other actions
            return [permissions.IsAdminUser(), IsProfileOwner()]


    

    def get_object(self):    
        return super().get_object()


    def get_queryset(self):
        queryset = super().get_queryset()

        specialization = self.request.query_params.get('specialization', None)
        city = self.request.query_params.get('city', None)
        area = self.request.query_params.get('area', None)
        if specialization is not None:
            queryset = queryset.filter(doctor__specialization__specialization=specialization)
        if city is not None:
            queryset = queryset.filter(doctor__address__location__city=city)
        if area is not None:
            queryset = queryset.filter(doctor__address__name=area)

        return self.queryset.order_by("id")




class Logout(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get the token
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)

            # Blacklist the token
            outstanding_token, _ = OutstandingToken.objects.get_or_create(
                token=str(token)
            )
            BlacklistedToken.objects.create(token=outstanding_token)

            # Perform any additional actions or cleanup
            # For example, you can delete any session-related data

            return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        except:
            return Response(
                {"detail": "Token is blacklisted"}, status=status.HTTP_400_BAD_REQUEST
            )


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """

    # serializer_class = ChangePasswordSerializer
    model = DoctorExtended
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)