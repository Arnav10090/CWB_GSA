from django.contrib import admin

from .models import DriverHelper, DriverVehicleTagging, DocumentControl, Users, VehicleDetails, Zone, ZoneType


admin.site.register(Users)
admin.site.register(ZoneType)
admin.site.register(Zone)
admin.site.register(VehicleDetails)
admin.site.register(DriverHelper)
admin.site.register(DriverVehicleTagging)
admin.site.register(DocumentControl)
