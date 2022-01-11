from django.urls import path
from apps.products.views import ProductViewSet,EnvProViewSet

urlpatterns = [
    path('list', ProductViewSet.as_view({'get': 'get', 'post': 'post', })),
    path('list/<pk>', ProductViewSet.as_view({'get': 'get_retrieve', 'update': 'update', 'delete': 'delete', })),
    path('env', EnvProViewSet.as_view({'get': 'get', 'post': 'post', })),
    path('env/<pk>', EnvProViewSet.as_view({'get': 'get_retrieve', 'update': 'update', 'delete': 'delete', })),
]
