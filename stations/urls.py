from django.urls import path
from .views import StationAPIView

urlpatterns = [
    path('stations/', StationAPIView.as_view(), name='station-list'),
]