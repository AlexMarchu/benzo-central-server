from django.contrib import admin
from users.models import User, Manager, LoyaltyCard

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'car_number', 'phone')
    search_fields = ('username', 'email', 'car_number', 'phone', 'first_name', 'last_name')

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('user', 'gas_station')
    search_fields = ('user__username', 'user__email', 'gas_station__address')
    
@admin.register(LoyaltyCard)
class LoyaltyCardAdmin(admin.ModelAdmin):
    list_display = ('number', 'balance')
    search_fields = ('number',)