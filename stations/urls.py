from django.urls import path
from .views import StationAPIView, GasStationAPIView

urlpatterns = [
    path('stations/', StationAPIView.as_view(), name='station-list'),
    path('gas-stations/', GasStationAPIView.as_view(), name='gas-station-list'),
]