from rest_framework import serializers
from schoolbus.models import Bus, BusPoint, Route
from student.models import Student
from admins.serializers import UserStudentSerializer
from teacher.models import ClassRoom

class BusPointSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusPoint
        fields = ["id", "route", "name", "fee"]


class StudentClassSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = ClassRoom
        fields = ['id', 'name','division']
        
class BusStudentSerializer(serializers.ModelSerializer):
    user = UserStudentSerializer()
    classRoom = StudentClassSerializer()
    class Meta:
        model = Student
        fields = [
            "id",
            "admission_no",
            # "guardian_name",
            # "pincode",
            # "house_name",
            # "post_office",
            "place",    
            "classRoom",
            "user",
        ]

class RouteSerializer(serializers.ModelSerializer):
    bus_points = BusPointSerializer(many=True, read_only=True)
    students = BusStudentSerializer(many=True, read_only=True)
    class Meta:
        model = Route
        fields = ["id", "bus", "route_no", "from_location", "to_location", "bus_points","students"]

    def update(self, instance, validated_data):
        instance.bus = validated_data.get("bus", instance.bus)
        instance.route_no = validated_data.get("route_no", instance.route_no)
        instance.from_location = validated_data.get(
            "from_location", instance.from_location
        )
        instance.to_location = validated_data.get("to_location", instance.to_location)

        instance.save()
        return instance


class BusSerializer(serializers.ModelSerializer):
    routes = RouteSerializer(many=True, read_only=True)
    # students = 

    class Meta:
        model = Bus
        fields = ["id", "bus_no", "driver_name", "plate_number", "capacity", "routes"]

    def update(self, instance, validated_data):
        instance.bus_no = validated_data.get("bus_no", instance.bus_no)
        instance.driver_name = validated_data.get("driver_name", instance.driver_name)
        instance.plate_number = validated_data.get(
            "plate_number", instance.plate_number
        )
        instance.capacity = validated_data.get("capacity", instance.capacity)

        instance.save()
        return instance
