from django.contrib import admin
from .models import Bus, Route, BusPoint


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ("id", "bus_no", "driver_name", "plate_number", "capacity")


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("id", "bus", "route_no", "from_location", "to_location")


@admin.register(BusPoint)
class BusPointAdmin(admin.ModelAdmin):
    list_display = ("id", "route", "name", "fee")
