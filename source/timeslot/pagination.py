from rest_framework.pagination import PageNumberPagination



class TimeSlotListPagination(PageNumberPagination):
    page_size = 2  # Number of results per page
    page_size_query_param = 'page_size'
    max_page_size = 100