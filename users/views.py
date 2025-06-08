from django.http import Http404
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import User, LoyaltyCard
from stations.models import GasStationLog
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserDetailSerializer,
    UserUpdateSerializer,
    LoyaltyCardSerializer,
    PaymentHistorySerializer,
)

class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            loyalty_card = LoyaltyCard.objects.create(
                number=serializer.generate_loyalty_card_number(),
                balance=0
            )

            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
                loyalty_card=loyalty_card
            )
            token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

class UserUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            if 'password' in serializer.validated_data:
                request.user.set_password(serializer.validated_data['password'])
                request.user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoyaltyCardView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if not hasattr(request.user, 'loyalty_card'):
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LoyaltyCardSerializer(request.user.loyalty_card)
        return Response(serializer.data)
    
class UserPaymentHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        logs = GasStationLog.objects.filter(user=request.user)
        if not logs.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PaymentHistorySerializer(logs, many=True)
        return Response({'history': serializer.data})
