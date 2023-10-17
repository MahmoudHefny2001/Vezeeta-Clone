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
    DoctorProfileSerializerForDoctors,
    DoctorProfileSerialzerForAppointmentDisplay,

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
from .permissions import IsObjectOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend 
 
from django.db.models import Q

from rest_framework_word_filter import FullWordSearchFilter

from .pagination import DoctorListPagination

from specialization.choices import SPECIAIALIZATION_CHOICES
from geo.choices import CITY_CHOICES, AREA_OR_CENTER_CHOICES 

from rest_framework.permissions import SAFE_METHODS

from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAdminUser, 
    IsAuthenticated, AllowAny, 
)

from specialization.serializers import SpecializationSerializer

from geo.models import Address, Location
from geo.serializers import LocationSerializer, AddressSerializer

from django.utils import timezone


class DoctorRegistrationView(views.APIView):
    permission_classes = [AllowAny,]
    
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    
    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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
        # 'doctor__full_name',
        # 'doctor__specialization__specialization',
        'doctor__qualifications',
        'doctor__address__name',
        'doctor__address__location__city',
    )

    filterset_fields = [
        # 'doctor__full_name',
        'doctor__address__name',
        'doctor__address__location__city',
        # 'doctor__specialization__specialization',
        'doctor__qualifications',    
    ] 

    
    search_fields = [  
        '@doctor__specialization__specialization',
        '@doctor__address__name',
        '@doctor__address__location__city',
        '@doctor__full_name',
        '@doctor__qualifications',
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
            return [permissions.IsAdminUser(), IsObjectOwnerOrReadOnly()]


    

    # def get_object(self):    
        # return super().get_object()


    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.prefetch_related('available_date').select_related('doctor')

        doctor_name = self.request.query_params.get('doctor_full_name', None)
        
        doctor_specialization = self.request.query_params.get('doctor_specialization', None)
        
        full_text_search = self.request.query_params.get('text_search', None)

        doctor_city = self.request.query_params.get('doctor_city', None)
        doctor_area = self.request.query_params.get('doctor_area', None)

        # Create Q objects for each query parameter
        conditions = Q()

        if doctor_name:
            conditions |= Q(doctor__full_name__icontains=doctor_name)


        if doctor_specialization:
            
            for specialization in SPECIAIALIZATION_CHOICES:
                if doctor_specialization.lower() == specialization[1].lower():
                    doctor_specialization = specialization[0]
                    print(doctor_specialization)
                    queryset = queryset.filter(doctor__specialization__specialization=doctor_specialization)

        if doctor_city:
            for city in CITY_CHOICES:
                if doctor_city.lower == city[1].lower():
                    doctor_city = city[0]
                    queryset = queryset.filter(doctor__address__location__city=doctor_city)


        if doctor_area:
            for area in AREA_OR_CENTER_CHOICES:
                if doctor_area.lower == area[1].lower():
                    doctor_area = area[0]
                    queryset = queryset.filter(doctor__address__name=doctor_area)


    
        # if specialization is not None:
        #     queryset = queryset.filter(doctor__specialization__specialization=specialization)
        # if city is not None:
        #     queryset = queryset.filter(doctor__address__location__city=city)
        # if area is not None:
        #     queryset = queryset.filter(doctor__address__name=area)

        if conditions:
            queryset = queryset.filter(conditions).order_by('id')
            
        # queryset = queryset.filter(available_date__date__gte=timezone.now()).order_by('id')
        return queryset.order_by('id')



class DoctorProfileViewSetForDoctors(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializerForDoctors
    authentication_classes = [JWTAuthentication,]
    permission_classes = [IsObjectOwnerOrReadOnly,]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]


    def get_permissions(self):
        return [IsObjectOwnerOrReadOnly()]
    

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        doctor_data = request.data.get('doctor', {})  # Access 'doctor' directly

        specialization_data = doctor_data.get('specialization', {})  # Access 'specialization' within 'doctor'        

        address_data = doctor_data.get('address', {})  # Access 'address' within 'doctor'
        
        if doctor_data:
            doctor_serializer = DoctorSerializer(instance.doctor, data=doctor_data, partial=True)
            if doctor_serializer.is_valid():
                doctor_serializer.save()

        if specialization_data:
            specialization_serializer = SpecializationSerializer(instance.doctor.specialization, data=specialization_data, partial=True)
            if specialization_serializer.is_valid():
                specialization_serializer.save()
        

        if address_data:
            # location_data = address_data.pop('location', {})  # Access 'location' within 'address'
            # if location_data:
                
            #     location_serializer = LocationSerializer(instance.doctor.address.location, data=location_data, partial=True)
            #     if location_serializer.is_valid():
            #         location_serializer.save()            
            address_serializer = AddressSerializer(instance.doctor.address, data=address_data, partial=True)
            if address_serializer.is_valid():
                address_serializer.save()


        serializer = self.get_serializer(instance, data=doctor_data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)
    

    def partial_update(self, request, *args, **kwargs):        
        instance = self.get_object()
        
        full_name = request.data.get("full_name", None)
        if full_name:
            instance.doctor.full_name = full_name
            instance.doctor.save()
        
        image = request.data.get("image", None)
        if image:
            instance.doctor.image = image
            instance.doctor.save()

        qualifications = request.data.get("qualifications", None)
        if qualifications:
            instance.doctor.qualifications = qualifications
            instance.doctor.save()
            
        appointment_price = request.data.get("appointment_price", None)
        if appointment_price:
            instance.doctor.appointment_price = appointment_price
            instance.doctor.save()
        clinic_number = request.data.get("clinic_number", None)
        if clinic_number:
            instance.doctor.clinic_number = clinic_number
            instance.doctor.save()
        gender = request.data.get("gender", None)
        if gender:
            instance.doctor.gender = gender
            instance.doctor.save()

        phone_number = request.data.get("phone_number", None)
        if phone_number:
            instance.doctor.phone_number = phone_number
            instance.doctor.save()
            
        email = request.data.get("email", None)
        if email:
            instance.doctor.email = email
            instance.doctor.save()

        specialization = request.data.get("specialization", None)
        print("view:", specialization)
        if specialization:
            specialization_serializer = SpecializationSerializer(instance.doctor.specialization, data=specialization, partial=True)
            if specialization_serializer.is_valid():
                specialization_serializer.save()
        
        address = request.data.get("address", None)
        if address:
            address_serializer = AddressSerializer(instance.doctor.address, data=address, partial=True)
            if address_serializer.is_valid():
                address_serializer.save()

        return super().partial_update(request, *args, **kwargs)
        

