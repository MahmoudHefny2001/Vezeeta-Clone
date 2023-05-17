import django_filters
from .models import Doctor, DoctorProfile

class DoctorFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    
    # location = django_filters.CharFilter(lookup_expr='icontains')
    # Add more filters as needed

    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name']  # Specify the fields you want to filter on