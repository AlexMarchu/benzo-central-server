from django.db import models

class FuelType(models.TextChoices):
    PETROL_92 = ('92', '92')
    PETROL_95 = ('95', '95')
    PETROL_98 = ('98', '98')
    DIESEL = ('DT', 'DT')

class PaymentMethod(models.TextChoices):
    CASH = ('cash', 'Cash')
    CARD = ('card', 'Card')
    LOYALTY = ('loyalty', 'Loyalty')

class GasStation(models.Model):
    address = models.TextField()

    def __str__(self):
        return self.address
    
class Station(models.Model):
    status = models.BooleanField(default=False)
    gas_station = models.ForeignKey(GasStation, on_delete=models.CASCADE, related_name='stations')

    def __str__(self):
        return f'Station {self.id} as {self.gas_station.address}'

class Fuel(models.Model):
    fuel_type = models.TextField(max_length=2, choices=FuelType.choices)
    amount = models.PositiveIntegerField() # centiliters
    price = models.PositiveIntegerField() # kopecks
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='fuels')

    class Meta:
        unique_together = ["station", "fuel_type"]

    def __str__(self):
        return f'{self.fuel_type} at {self.station.gas_station.address}'
