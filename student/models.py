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
    is_bus = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.user.name
    
class StudentBusService(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='bus_service')
    bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True, blank=True)
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True)
    bus_point = models.ForeignKey(BusPoint, on_delete=models.SET_NULL, null=True, blank=True)
    annual_fees = models.IntegerField(null=True, blank=True)

    
    def __str__(self) -> str:
        return f"{self.student.user.name} is in {self.bus.bus_no} rout no:{self.route.route_no} to {self.bus_point.name}"