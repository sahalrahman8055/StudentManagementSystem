from django.contrib import admin
from teacher.models import ClassRoom , Teacher
# Register your models here.


admin.site.register(Teacher)
@admin.register(ClassRoom)
class ClassROomAdmin(admin.ModelAdmin):
    list_display = ('id','name','capacity')