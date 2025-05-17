# views.py
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .serializers import StationSerializer, GasStationSerializer
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
