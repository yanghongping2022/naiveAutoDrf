# 自定义分页对象
from rest_framework.pagination import PageNumberPagination


class BasePageNumberPagination(PageNumberPagination):
    # 1,默认的大小
    page_size = 10
    # 2,前端可以指定页面大小
    page_size_query_param = 'pagesize'
    # # 3,页面的最大大小
    # max_page_size = 100
