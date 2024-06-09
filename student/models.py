from django.db import models
from admins.models import User
from teacher.models import ClassRoom
from schoolbus.models import Bus, Route, BusPoint
from decimal import Decimal

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admission_no = models.CharField(max_length=15, unique=True)
    guardian_name = models.CharField(max_length=150)
    address = models.TextField(max_length=250, blank=True, null=True)
    classRoom = models.ForeignKey(
        ClassRoom,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="students",
    )
    is_bus = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.name


class StudentBusService(models.Model):
    student = models.OneToOneField(
        Student, on_delete=models.CASCADE, related_name="bus_service"
    )
    bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True, blank=True)
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True)
    bus_point = models.ForeignKey(
        BusPoint, on_delete=models.SET_NULL, null=True, blank=True
    )
    annual_fees = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.student.user.name} is in {self.bus.bus_no} route no:{self.route.route_no} to {self.bus_point.name}"


class Payment(models.Model):
    PAYMENT_METHOD = [
        ("UPI", "UPI"),
        ("CASH", "CASH"),
    ]
    bus_service = models.ForeignKey(
        StudentBusService, on_delete=models.CASCADE, related_name="payments"
    )
    method = models.CharField(blank=True,null=True, choices=PAYMENT_METHOD)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment: {self.amount} (Method: {self.method})'
    
    def save(self, *args, **kwargs):
        # If the instance already exists, revert the old amount
        if self.pk:
            old_instance = Payment.objects.get(pk=self.pk)
            self.bus_service.annual_fees += Decimal(old_instance.amount)

        self.bus_service.annual_fees -= Decimal(self.amount)
        self.bus_service.save()
        
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Revert the amount when the payment is deleted
        self.bus_service.annual_fees += Decimal(self.amount)
        self.bus_service.save()
        super().delete(*args, **kwargs)
    
