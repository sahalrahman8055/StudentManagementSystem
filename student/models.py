from django.db import models
from admins.models import User
from teacher.models import ClassRoom
from schoolbus.models import Bus , Route , BusPoint


class Student(models.Model):
    user =  models.OneToOneField(User, on_delete=models.CASCADE)
    admission_no = models.CharField(max_length=15,unique=True)
    guardian_name = models.CharField(max_length=150)
    address = models.TextField(max_length=250,blank=True,null=True)
    classRoom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, blank=True,null=True, related_name='students')
    bus = models.ForeignKey(Bus, related_name='students', on_delete=models.SET_NULL, null=True)
    route = models.ForeignKey(Route, related_name='students', on_delete=models.SET_NULL, null=True)
    bus_point = models.ForeignKey(BusPoint, related_name='students', on_delete=models.SET_NULL, null=True)
    
    def __str__(self) -> str:
        return self.user.name