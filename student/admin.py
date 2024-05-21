from django.contrib import admin
from .models import Student , StudentBusService


admin.site.register(Student)

@admin.register(StudentBusService)
class BusAdmin(admin.ModelAdmin):
    list_display = ('id','student', 'bus', 'route', 'bus_point','annual_fees')
    


