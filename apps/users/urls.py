from django.urls import path
from apps.users.views import LoginAPIView,UserViewSet

urlpatterns = [
    path('sign', LoginAPIView.as_view({'post': 'post'})),
    path('info', UserViewSet.as_view({'get': 'get'})),
]
