from django.contrib import admin
from admins.models import User


@admin.register(User)
class BusAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
