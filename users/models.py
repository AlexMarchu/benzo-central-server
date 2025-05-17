from django.db import models
from django.contrib.auth.models import AbstractUser

from stations.models import GasStation

class LoyaltyCard(models.Model):
    number = models.CharField(32, unique=True)
    balance = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Card {self.number}'

class User(AbstractUser):
    car_number = models.CharField(max_length=20, blank=True, null=True)
    penalty = models.PositiveIntegerField(default=0)
    loyalty_card = models.OneToOneField(LoyaltyCard, on_delete=models.SET_NULL, blank=True, null=True)

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager_profile')
    gas_station = models.ForeignKey(GasStation, on_delete=models.CASCADE, related_name='managers')

    def __str__(self):
        return f'Manager {self.user.username} for {self.gas_station}'