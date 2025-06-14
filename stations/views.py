from django.shortcuts import render, get_object_or_404
from django.db.models import CharField
from django.db.models.functions import Cast
from rest_framework import generics, status, views
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .serializers import StationSerializer, GasStationSerializer, FuelInfoSerializer, GasStationListSerializer, StationStatusSerializer
from .models import GasStation, Station, FuelType

class StationAPIView(generics.ListAPIView):
    serializer_class = StationSerializer

    def get_queryset(self):
        fuel_type = self.request.query_params.get('fuel')
        
        if not fuel_type:
            raise ValidationError({'error': 'fuel parameter is required'})
        
        if fuel_type not in FuelType.values:
            raise ValidationError({'error': f'Invalid fuel type. Available types: {", ".join(FuelType.values)}'})
        
        return Station.objects.filter(fuels__fuel_type=fuel_type).distinct()
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        
class GasStationAPIView(generics.ListAPIView):
    queryset = GasStation.objects.all()
    serializer_class = GasStationSerializer

class GasStationListView(generics.ListAPIView):
    serializer_class = GasStationListSerializer

    def get_queryset(self):
        queryset = GasStation.objects.all()
        address_prefix = self.request.query_params.get('address')
        id_prefix = self.request.query_params.get('id')

        if address_prefix:
            queryset = queryset.filter(address__istartswith=address_prefix)
        if id_prefix:
            queryset = queryset.annotate(id_str=Cast('id', output_field=CharField())) \
                              .filter(id_str__startswith=id_prefix)

        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({'gas_stations': serializer.data})
    
class StationStatusView(views.APIView):
    def get(self, request, gas_station_id):
        gas_station = get_object_or_404(GasStation, id=gas_station_id)
        stations = gas_station.stations.all()
        serializer = StationStatusSerializer(stations, many=True)
        return Response({'stations': serializer.data})
    
class FuelInfoView(views.APIView):
    def get(self, request, station_id):
        station = get_object_or_404(Station, id=station_id)
        fuels = station.fuels.all()
        serializer = FuelInfoSerializer(fuels, many=True)
        return Response({'fuels': serializer.data})
    
class ReportProblemView(views.APIView):
    def post(self, request, station_id):
        # TODO: check token
        station = get_object_or_404(Station, id=station_id)
        description = request.data.get('description', '')
        # TODO: implement problem processing logic
        return Response({'status': 'Problem reported'}, status=status.HTTP_200_OK)
