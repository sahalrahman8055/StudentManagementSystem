from django.db import models
from admins.models import User
from teacher.models import ClassRoom
from schoolbus.models import Bus, Route, BusPoint
from decimal import Decimal
from django.db.models import Sum

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admission_no = models.CharField(max_length=15, unique=True)
    guardian_name = models.CharField(max_length=150)
    house_name = models.CharField(max_length=100, blank=True, null=True)
    post_office = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=6, blank=True, null=True)
    place = models.CharField(max_length=100, blank=True, null=True)
    route = models.ForeignKey(Route, related_name="students", on_delete=models.CASCADE,blank=True,null=True)
    classRoom = models.ForeignKey(
        ClassRoom,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="students",
    )
    is_bus = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.admission_no} - {self.user.name}"


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
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="payments"
    )
    method = models.CharField(blank=True,null=True, choices=PAYMENT_METHOD)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment: {self.amount} (Method: {self.method})'
    
    def save(self, *args, **kwargs):
        # Calculate total paid amount including this instance
        total_paid = Payment.objects.filter(student=self.student).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        total_paid += self.amount
        self.paid_amount = total_paid
        # Update balance amount
        self.balance_amount = self.student.bus_service.annual_fees - total_paid
        super().save(*args, **kwargs)
    
    # def save(self, *args, **kwargs):

    #     total_paid = self.student.payments.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    #     self.paid_amount = total_paid
    #     # Update balance amount
    #     self.balance_amount = self.student.bus_service.annual_fees - total_paid
    #     super().save(*args, **kwargs)
    
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)  # Save the payment first

    #     # Calculate total paid amount for the student
    #     total_paid = self.student.payments.aggregate(total=Sum('amount'))['total'] or 0

    #     # Calculate balance amount
    #     annual_fees = self.student.bus_service.annual_fees
    #     balance_amount = annual_fees - total_paid

    #     # Update the representation of this payment instance
    #     self.paid_amount = total_paid
    #     self.balance_amount = balance_amount
    #     self.save(update_fields=['paid_amount', 'balance_amount'])  # Save the updated fields

    # def delete(self, *args, **kwargs):
    #     # Calculate total paid amount for the student
    #     total_paid = self.student.payments.aggregate(total=Sum('amount'))['total'] or 0

    #     # Calculate balance amount
    #     annual_fees = self.student.bus_service.annual_fees
    #     balance_amount = annual_fees - total_paid

    #     # Update the representation of this payment instance
    #     self.paid_amount = total_paid
    #     self.balance_amount = balance_amount
    #     self.save(update_fields=['paid_amount', 'balance_amount'])  # Save the updated fields

    #     super().delete(*args, **kwargs)
    
