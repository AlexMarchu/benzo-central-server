from django.contrib import admin
from stations.models import GasStation, Station, Fuel, GasStationLog

class FuelInline(admin.TabularInline):
    model = Fuel
    extra = 0
    fields = ('fuel_type', 'amount', 'price')
    readonly_fields = ('fuel_type', 'amount', 'price')

class StationInline(admin.TabularInline):
    model = Station
    extra = 0
    fields = ('status',)
    show_change_link = True
    readonly_fields = ('status',)

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    inlines = [FuelInline]
    list_display = ('id', 'gas_station', 'status', 'fuels_list')
    list_filter = ('status', 'gas_station')
    search_fields = ('gas_station__address',)
    
    def fuels_list(self, obj):
        return ", ".join([f.fuel_type for f in obj.fuels.all()])
    fuels_list.short_description = 'Available Fuels'

@admin.register(GasStation)
class GasStationAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'stations_count')
    inlines = [StationInline]
    search_fields = ('address',)
    
    def stations_count(self, obj):
        return obj.stations.count()
    stations_count.short_description = 'Number of Stations'

@admin.register(Fuel)
class FuelAdmin(admin.ModelAdmin):
    list_display = ('id', 'station', 'fuel_type', 'price_display', 'amount_display')
    list_filter = ('fuel_type',)
    search_fields = ('station__gas_station__address', 'fuel_type')
    
    def price_display(self, obj):
        return f"{obj.price / 100:.2f} ₽"
    price_display.short_description = 'Price'
    
    def amount_display(self, obj):
        return f"{obj.amount / 100:.1f} L"
    amount_display.short_description = 'Amount'

@admin.register(GasStationLog)
class GasStationLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_time', 'station', 'fuel_type', 'fuel_amount', 'payment_amount')
    list_filter = ('fuel_type',)
    readonly_fields = ('date_time',)
    search_fields = ('station__gas_station__address', 'fuel_type', 'car_number', 'payment_key')