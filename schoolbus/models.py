from typing import Iterable
from django.db import models




class Bus(models.Model):
    bus_no = models.PositiveSmallIntegerField(unique=True)
    driver_name = models.CharField(max_length=150, blank=True, null=True)
    plate_number = models.CharField(max_length=15, blank=True, null=True)
    capacity = models.PositiveIntegerField(default=50)

    def __str__(self):
        return f"Bus {self.bus_no} - {self.plate_number}"



class Route(models.Model):
    bus = models.ForeignKey(Bus, related_name='routes', on_delete=models.CASCADE)
    route_no = models.PositiveSmallIntegerField()
    from_location = models.CharField(max_length=255)
    to_location = models.CharField(max_length=255)

    class Meta:
        unique_together = ('bus', 'route_no')

    def __str__(self):
        return f"Route {self.route_no} for Bus {self.bus.bus_no}"



class BusPoint(models.Model):
    route = models.ForeignKey(Route, related_name='bus_points', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    def save(self, *args, **kwargs):
        fees = BusPoint.objects.get(id=self.pk)
        if not self.pk and self.fee!= fees.fee:
            from student.models import Student
            # print(self.fee,fees.fee)
            student=Student.objects.filter()
            pass
        super(BusPoint, self).save(*args, **kwargs)
        #     pass

    def __str__(self):
        return f"Bus Point {self.name} on Route {self.route.route_no} for Bus {self.route.bus.bus_no}"
