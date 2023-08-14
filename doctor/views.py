from django.shortcuts import render
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
    # OuterViewDoctorProfileSerializer,
    #ChangePasswordSerializer,
    #DoctorProfileSerializerForDoctors,
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
from .filters import PartialSearchFilter, DoctorFilter
from review.models import Review
from review.serializers import ReviewSerializer
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.pagination import PageNumberPagination
from .permissions import IsProfileOwner
from django_filters.rest_framework import DjangoFilterBackend 
 
from django.db.models import Q



class DoctorListPagination(PageNumberPagination):
    page_size = 10  # Number of results per page
    page_size_query_param = 'page_size'
    max_page_size = 100



class DoctorRegistrationView(views.APIView):
    permission_classes = [AllowAny,]
    
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    

    def post(self, request):
        try:
            serializer = DoctorSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Exception as e:
            print(e)
            raise e


class LoginView(views.APIView):
    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]


    def post(self, request):
        email_or_phone = request.data.get("email_or_phone")
        password = request.data.get("password")
        doctor = CustomUserAuthBackend().authenticate(
            request=request, username=email_or_phone, password=password
        )

        doctor_prfile_id = DoctorProfile.objects.filter(doctor=doctor).first().id
        
        doctor_name = DoctorProfile.objects.filter(doctor=doctor).first().doctor.full_name

        if doctor is not None:
            access_token = AccessToken.for_user(doctor)
            refresh_token = RefreshToken.for_user(doctor)
            return Response(
                {
                    "access": str(access_token),
                    "refresh": str(refresh_token),

                    "doctor_profile_id": doctor_prfile_id,
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


SPECIALIZATION_CHOICES_DICT = {
    '1': "جلدية",
    '2': "اسنان",
    '3': "نفسي",
    '4': "عظام",
    '5': "اطفال وحديثي الولادة",
    '6': "مخ واعصاب",
    '7': "نساءوتوليد",
    '8': "انف واذن وحجره",
    '9': "قلب واوعبة دموية",
    '10': "أمراض الدم",
    '11': "باطنة",
    '12': "تخسيس وتغذية",
    '13': "جراحة اطفال",
    '14': "جراحة اورام",
    '15': "جراحة اوعية دمويه",
    '16': "جراحة تجميل",
    '17': "جراحة سمنة وماظير",
    '18': "جراحة عامة",
    '19': "جراحة عمود فقري",
    '20': "جراحة قلب وصدر",
    '21': "جراحة مخ واعصاب",
    '22': "حساسية ومناعة",
    '23': "حقن مجهري واطفال انابيب",
    '24': "ذكورة وعقم",
    '25': "روماتيزم",
    '26': "سمعيات",
    '27': "صدر وجهاز تنفسي",
    '28': "طب الاسرة",
    '29': "طب تقويمي",
    '30': "علاج الآلام",
    '31': "علاج طبيعي واصابات ملاعب",
    '32': "عيون",
    '33': "كبد",
    '34': "كلي",
    '35': "مراكز اشعة",
    '36': "مسالك بوليه",
    '37': "ممارسة عامة",
    '39': "نطق وتخاطب"
}


class DoctorProfileViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = DoctorListPagination

    queryset = DoctorProfile.objects.all()
    
    permission_classes = [IsAuthenticatedOrReadOnly]

    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter, 
        PartialSearchFilter,
    ]
    
    filter_class = DoctorFilter
    

    filterset_fields = [
        'doctor__full_name',
        'doctor__area_or_center',
        'doctor__specialization',
        'doctor__location',
        'doctor__qualifications',
    ] 

    search_fields = [  
        # Search fields for the search filter
        '@doctor__specialization',
        '@doctor__area_or_center'
        '@doctor__full_name',
        '@doctor__specialization',
        '@doctor__qualifications',
    ]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            # Allow any user to list and retrieve doctors
            return [permissions.AllowAny()]
        else:
            # Only authenticated users can perform other actions
            return [permissions.IsAdminUser(), IsProfileOwner()]


    def get_serializer_class(self):
        if self.action == "list":
            return OuterViewDoctorProfileSerializer
        return DoctorProfileSerializer
    
    
    def get_object(self):
        
        return super().get_object()


    
    def get_queryset(self):
        
        queryset = DoctorProfile.objects.all()
        
        specialization = self.request.query_params.get('doctor__specialization')
        if specialization is not None:
            print(specialization)
            # Build a query to match any of the specialization numbers
            specialization_choice = SPECIALIZATION_CHOICES_DICT[specialization]
            print(specialization_choice)

            queryset = queryset.filter(doctor__specialization=specialization_choice)
            print(queryset.values())
            
        
        return queryset.order_by("id")
    

    def get_filter_backends(self):
        filter_backends = super().get_filter_backends()
        search_fields = self.search_fields + [f"^{field}" for field in self.search_fields]

        return filter_backends + [PartialSearchFilter(search_fields=search_fields)]




class DoctorProfileViewSet_Doctors(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.all()
    # serializer_class = DoctorProfileSerializerForDoctors
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    pagination_class = DoctorListPagination


    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            # Allow any user to list and retrieve doctors
            return [permissions.AllowAny()]
        else:
            # Only authenticated users can perform other actions
            return [permissions.IsAuthenticated()]


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
