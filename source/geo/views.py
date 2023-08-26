from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    AllowAny,
)
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from . import models, serializers

from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework import filters
from rest_framework_word_filter import FullWordSearchFilter
from rest_framework import generics



class AddressViewSet(ModelViewSet):
    queryset = models.Address.objects.all()
    serializer_class = serializers.GeoAddressSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    permission_classes = [AllowAny,]

    # Make Allowed methods to be only GET and HEAD
    http_method_names = ['get', 'head', 'options']

    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter, 
        FullWordSearchFilter,
    ]


    word_fields = (
        'name',
        'location__city',
    )

    filterset_fields = [
        'name',
        'location__city',
    ] 

    
    search_fields = [  
        'name',
        'location__city',
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        # location__city = self.request.query_params.get('location__city', None)
        # if location__city:
        #     # Remove Duplicate Values
        #     queryset = queryset.filter(location__city=location__city).distinct('location_id')
        # return queryset.order_by('id')

        city = self.request.query_params.get('city', None)
        if city:
            queryset = queryset.filter(location__city=city)

        return queryset.order_by('location__city', 'name').distinct('location__city', 'name')
    


class CitiesListView(generics.ListAPIView):
    queryset = models.Location.objects.all()
    serializer_class = serializers.GeoLocationSerializer
    permission_classes = [AllowAny,]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    # Make Allowed methods to be only GET and HEAD
    http_method_names = ['get', 'head', 'options']


    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.order_by('city', 'id').distinct('city')
    