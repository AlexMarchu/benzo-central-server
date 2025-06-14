from rest_framework import serializers
from django.contrib.auth import authenticate

from users.models import User, LoyaltyCard
from stations.models import GasStationLog

class UserRegisterSerializer(serializers.ModelSerializer):
    login = serializers.CharField(source='username')

    class Meta:
        model = User
        fields = ('login', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Login is taken')
        return value
    
    def generate_loyalty_card_number(self):
        import random
        while True:
            card_number = f'{random.randint(1, 9)}{''.join(f'{random.randint(0, 9)}' for _ in range(6))}'
            if not LoyaltyCard.objects.filter(number=card_number).exists():
                return card_number

class UserLoginSerializer(serializers.Serializer):
    login = serializers.CharField(source='username')
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid login or password')
        return user

class UserDetailSerializer(serializers.ModelSerializer):
    login = serializers.CharField(source='username')
    name = serializers.CharField(source='first_name', allow_null=True)
    phone_number = serializers.CharField(source='phone', allow_null=True)
    birth_date = serializers.DateField(format='%Y-%m-%d', allow_null=True)  # (YYYY-MM-DD)

    class Meta:
        model = User
        fields = ('login', 'name', 'birth_date', 'car_number', 'phone_number', 'email', 'gender')

class UserUpdateSerializer(serializers.ModelSerializer):
    login = serializers.CharField(source='username', required=False)
    name = serializers.CharField(source='first_name', required=False)
    phone_number = serializers.CharField(source='phone', allow_null=True)
    birth_date = serializers.DateField(format='%Y-%m-%d', required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('login', 'password', 'name', 'birth_date', 'car_number', 'phone_number', 'email', 'gender')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }

class LoyaltyCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyCard
        fields = ('number', 'balance')

class PaymentHistorySerializer(serializers.ModelSerializer):
    gas_station_id = serializers.IntegerField(source='station.gas_station.id')
    gas_station_address = serializers.CharField(source='station.gas_station.address')
    station_id = serializers.IntegerField(source='station.id')
    bonuses_used = serializers.SerializerMethodField()
    user_id = serializers.IntegerField(source='user.id', allow_null=True)

    class Meta:
        model = GasStationLog
        fields = ('date_time', 'gas_station_id', 'user_id', 'gas_station_address', 'station_id', 'fuel_type',
                  'fuel_amount', 'car_number', 'payment_amount', 'bonuses_used', 'payment_key')
        
    def get_bonuses_used(self, obj):
        return obj.bonuses_used
