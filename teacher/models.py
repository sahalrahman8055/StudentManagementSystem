from django.db import models
from admins.models import User



class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pen_no = models.CharField(max_length=15,unique=True)
    short = models.CharField(max_length=5,blank=True,null=True)
    
    def __str__(self):
        return self.user.name



class ClassRoom(models.Model):
    users = models.ManyToManyField(User, related_name='classrooms', blank=True)
    name = models.CharField(max_length=150,unique=True)
    capacity = models.PositiveIntegerField()
    
    def __str__(self) :
        return self.name
      
    