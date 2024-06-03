from django.contrib import admin
from teacher.models import ClassRoom , Teacher
# Register your models here.


@admin.register(ClassRoom)
class ClassROomAdmin(admin.ModelAdmin):
    list_display = ('id','name','capacity')
    
@admin.register(Teacher)
class ClassROomAdmin(admin.ModelAdmin):
    list_display = ('id','user','pen_no')