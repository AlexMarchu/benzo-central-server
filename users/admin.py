from django.contrib import admin
from users.models import User, Manager, LoyaltyCard

admin.site.register(User)
admin.site.register(Manager)
admin.site.register(LoyaltyCard)
