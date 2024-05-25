from django.contrib import admin
from .models import Student , StudentBusService



@admin.register(StudentBusService)
class BusAdmin(admin.ModelAdmin):
    list_display = ('id','student', 'bus', 'route', 'bus_point','annual_fees')
    
    
admin.register(StudentBusService)
@admin.register(Student)
class BusAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'admission_no', 'classRoom',)
    


