from rest_framework.pagination import PageNumberPagination


class StandardSizePagination(PageNumberPagination):
    page_size = 50
