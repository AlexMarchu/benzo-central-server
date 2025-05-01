from django.db import models

class FuelType(models.TextChoices):
    PETROL_92 = ('92', '92')
    PETROL_95 = ('95', '95')
    PETROL_98 = ('98', '98')
    DIESEL = ('DT', 'DT')

class Station(models.Model):
    address = models.TextField()

class FuelInfo(models.Model):
    fuel_type = models.TextField(choices=FuelType.choices)
    amount = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='fuels')

    class Meta:
        unique_together = ["station", "fuel_type"]
