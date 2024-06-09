from rest_framework import serializers
from schoolbus.models import Bus, BusPoint, Route
from rest_framework import serializers
from admins.models import User
from student.models import Student, StudentBusService
from teacher.models import ClassRoom, Teacher
from student.models import Payment
from decimal import Decimal

class TeacherLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class BusPointChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusPoint
        fields = ["id", "route", "name", "fee"]


class RouteChoiceSerializer(serializers.ModelSerializer):
    bus_points = BusPointChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Route
        fields = ["id", "bus", "route_no", "from_location", "to_location", "bus_points"]


class BusListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bus
        fields = ["id", "bus_no", "driver_name", "plate_number", "capacity"]


class StudentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "gender"]


class UserStudentSerializer(serializers.ModelSerializer):
    user = StudentListSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ["id", "admission_no", "user"]


class StudentSerializer(serializers.ModelSerializer):
    user = StudentListSerializer()

    class Meta:
        model = Student
        fields = ("admission_no", "user", "classRoom")
        read_only_fields = ("admission_no",)


class BusStudentSerializer(serializers.ModelSerializer):
    student = UserStudentSerializer()
    bus = BusListSerializer()
    route = RouteChoiceSerializer()
    bus_point = BusPointChoiceSerializer()

    class Meta:
        model = StudentBusService
        fields = ["student", "bus", "route", "bus_point"]


class PaymentSerializer(serializers.ModelSerializer):
    bus_service = serializers.PrimaryKeyRelatedField(queryset=StudentBusService.objects.all())
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    method = serializers.ChoiceField(choices=Payment.PAYMENT_METHOD)
    paid_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    balance_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)


    class Meta:
        model = Payment
        fields = ('id','bus_service', 'amount', 'method','paid_amount','balance_amount', 'created_at')

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Payment amount must be positive.")
        return value

    def validate(self, data):
        bus_service = data['bus_service']
        if bus_service.annual_fees < data['amount']:
            raise serializers.ValidationError("Payment amount exceeds the remaining total fees.")
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        bus_service = instance.bus_service
        amount_paid = instance.amount
        print(amount_paid)

        transactions = Payment.objects.filter(
            bus_service=bus_service,
            created_at__lte=instance.created_at
        )
        print(transactions,'999999')
        
        # Calculate the total paid amount including the current transaction
        total_paid = sum(transaction.amount for transaction in transactions)
        balance_amount = bus_service.annual_fees 

        representation['total_paid_amount'] = total_paid
        representation['balance_amount'] = balance_amount
        
        return representation

