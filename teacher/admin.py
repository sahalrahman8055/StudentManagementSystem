from django.contrib import admin
from teacher.models import ClassRoom, Teacher, ClassRoomTeacher 

# Register your models here.


admin.site.register(ClassRoomTeacher)


@admin.register(ClassRoom)
class ClassROomAdmin(admin.ModelAdmin):
    list_display = ("id", "name","capacity")


@admin.register(Teacher)
class ClassROomAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "pen_no")



