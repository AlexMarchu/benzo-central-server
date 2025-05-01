from rest_framework import serializers

from .models import Station, FuelInfo

class FuelInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelInfo
        fields = "__all__"

class FuelPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelInfo
        fields = ['price']

class StationSerializer(serializers.ModelSerializer):
    fuel_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Station
        fields = ['id', 'address', 'fuel_price']
    
    def get_fuel_price(self, obj):
        fuel_type = self.context['request'].query_params.get('fuel')
        fuel_info = obj.fuels.filter(fuel_type=fuel_type).first()
        return fuel_info.price if fuel_info else None