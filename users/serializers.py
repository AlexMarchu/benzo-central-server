from rest_framework import serializers
from django.contrib.auth import authenticate

from users.models import User, LoyaltyCard

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', '')
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'car_number', 'loyalty_card')

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'password')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'username': {'required': False},
            'first_name': {'required': False}
        }

class LoyaltyCardSerializer(serializers.ModelSerializer):
    balance_in_rubles = serializers.SerializerMethodField()
    
    class Meta:
        model = LoyaltyCard
        fields = ('number', 'balance', 'balance_in_rubles')
    
    def get_balance_in_rubles(self, obj):
        return obj.balance / 100