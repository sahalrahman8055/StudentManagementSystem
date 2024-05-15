from django.db import models
from admins.models import User
# Create your models here.


class Student(models.Model):
    user =  models.OneToOneField(User, on_delete=models.CASCADE)
    admission_no = models.CharField(max_length=15,unique=True)
    guardian_name = models.CharField(max_length=150)
    address = models.TextField(max_length=250,blank=True,null=True)
    
    def __str__(self) -> str:
        return self.user.name