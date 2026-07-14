"""
Pagination utilities for SGHL API
"""
from ninja.pagination import PageNumberPagination
from rest_framework.pagination import PageNumberPagination as DRFPageNumberPagination


class SGHLPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class StandardResultsSetPagination(DRFPageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
