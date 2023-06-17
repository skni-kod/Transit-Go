from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, BusStop, Vehicle, RaportsUnlogged
from mainContent.models import User

# Register your models here.
admin.site.register(User, UserAdmin)
@admin.register(BusStop)
class BusStopAdmin(admin.ModelAdmin):
    pass
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    pass
@admin.register(RaportsUnlogged)
class RaportsUnloggedAdmin(admin.ModelAdmin):
    pass