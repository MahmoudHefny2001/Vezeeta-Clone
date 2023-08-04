from rest_framework import filters
from django.db import models
import operator
from functools import reduce
import six
from .models import DoctorExtended, DoctorProfile

import django_filters

class DoctorFilter(django_filters.FilterSet):

    
    class Meta:
        
        model = DoctorProfile
        fields = {
            "doctor__first_name": ["contains", "startswith", "exact", "icontains",],
            "doctor__last_name": ["contains", "startswith", "exact", "icontains"],
            "doctor__specialization__speciality": ["startswith", "exact", "icontains", "contains"],
            "doctor__qualifications": ["startswith", "exact", "icontains", "contains"],
            "clinic__location__name": ["startswith", "exact", "icontains", "contains"],
        }
        together = ['doctor__first_name', 'doctor__last_name']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        


    def filter_queryset(self, queryset):
        print("Filtering with DoctorFilter:")
        print("Search terms:", self.form.cleaned_data)
        result = super().filter_queryset(queryset)
        print("Filtered queryset:", result)
        return result



class PartialSearchFilter(filters.SearchFilter):
    def __init__(self, *args, **kwargs):
        self.search_fields = kwargs.pop('search_fields', [])
        super().__init__(*args, **kwargs)
    

    def filter_queryset(self, request, queryset, view):
        search_param = self.get_search_terms(request)
        if not search_param or not self.search_fields:
            return queryset

        print("Filtering with PartialSearchFilter:")
        print("Search terms:", search_param)

        orm_lookups = [self.construct_search(six.text_type(search_term)) for search_term in search_param]
        conditions = []

        for search_field in self.search_fields:
            queries = [models.Q(**{search_field + '__icontains': term}) for term in search_param]
            conditions.extend(queries)

        if conditions:
            queryset = queryset.filter(reduce(operator.or_, conditions))

        print("Filtered queryset:", queryset)

        return queryset
