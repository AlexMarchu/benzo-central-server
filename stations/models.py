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

class StationStatus(models.TextChoices):
    BUSY_OFFLINE = ('busy_offline', 'Busy offline')
    BUSY_ONLINE = ('busy_online', 'Busy online')
    FREE = ('free', 'Free')
    NOT_WORKING = ('not_working', 'Not working')

class GasStation(models.Model):
    address = models.TextField()

    def __str__(self):
        return self.address
    
class Station(models.Model):
    status = models.CharField(max_length=32, choices=StationStatus.choices, default=StationStatus.FREE)
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

class GasStationLog(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    station = models.ForeignKey(Station, on_delete=models.SET_NULL, related_name='logs', null=True)
    fuel_type = models.CharField(max_length=2, choices=FuelType.choices)
    fuel_amount = models.PositiveIntegerField()
    car_number = models.CharField(max_length=20, blank=True, null=True)
    payment_amount = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices)
    payment_key = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Log #{self.id} at {self.date_time}'
