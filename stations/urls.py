from django.urls import path
from .views import (
    StationAPIView, 
    GasStationAPIView,
    GasStationListView,
    StationStatusView,
    FuelInfoView,
    ReportProblemView
)

urlpatterns = [
    path('stations/', StationAPIView.as_view(), name='station-list'),
    # path('gas-stations/', GasStationAPIView.as_view(), name='gas-station-list'),
    path('gas-stations/', GasStationListView.as_view(), name='gas-station-filtered-list'),
    path('gas-station/<int:gas_station_id>/stations/', StationStatusView.as_view(), name='station-status'),
    path('station/<int:station_id>/fuels/', FuelInfoView.as_view(), name='fuel-info'),
    path('station/<int:station_id>/report/', ReportProblemView.as_view(), name='report-problem'),
]