from django.contrib import admin
from stations.models import GasStation, Station, Fuel, FuelType

admin.site.register(GasStation)
admin.site.register(Station)
admin.site.register(Fuel)
