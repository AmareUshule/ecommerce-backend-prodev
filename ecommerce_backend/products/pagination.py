from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """PageNumberPagination that allows clients to set `?page_size=` up to a max."""
    page_size_query_param = 'page_size'
    max_page_size = 100
