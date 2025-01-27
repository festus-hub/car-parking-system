from django.contrib import admin
from django.contrib.auth.models import User
from .models import Vehicle
from .models import VehicleLocation


# Register your models here.
#admin.site.register(User)
# @admin.register(Vehicle)
# class VehicleAdmin(admin.ModelAdmin):
#     list_display = ('owner', 'license_plate', 'parked_at','parked_time','phone_number')
admin.site.register(Vehicle)
admin.site.register(VehicleLocation)

