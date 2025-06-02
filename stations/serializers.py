from rest_framework import serializers
from .models import GasStation, Station, Fuel, FuelType

class FuelSerializer(serializers.ModelSerializer):
    price_in_rubles = serializers.SerializerMethodField()
    amount_in_liters = serializers.SerializerMethodField()
    
    class Meta:
        model = Fuel
        fields = ['id', 'fuel_type', 'price', 'amount', 
                 'price_in_rubles', 'amount_in_liters', 'station']
    
    def get_price_in_rubles(self, obj):
        return obj.price / 100
    
    def get_amount_in_liters(self, obj):
        return obj.amount / 100

class StationSerializer(serializers.ModelSerializer):
    gas_station_address = serializers.CharField(source='gas_station.address', read_only=True)
    fuels = FuelSerializer(many=True, read_only=True)
    fuel_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Station
        fields = ['id', 'status', 'gas_station', 'gas_station_address', 
                 'fuels', 'fuel_price']
    
    def get_fuel_price(self, obj):
        fuel_type = self.context['request'].query_params.get('fuel')
        fuel = obj.fuels.filter(fuel_type=fuel_type).first()
        return fuel.price / 100 if fuel else None

class GasStationSerializer(serializers.ModelSerializer):
    stations = StationSerializer(many=True, read_only=True)
    
    class Meta:
        model = GasStation
        fields = ['id', 'address', 'stations']

class GasStationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GasStation
        fields = ['id', 'address']

class StationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ['id', 'status']

class FuelInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fuel
        fields = ['fuel_type', 'price', 'amount']
        