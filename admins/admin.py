from django.contrib import admin
from .models import User,Role
# Register your models here.


admin.site.register(Role)

@admin.register(User)
class BusAdmin(admin.ModelAdmin):
    list_display = ('id','name')