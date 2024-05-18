from rest_framework import serializers
from schoolbus.models import Bus,BusPoint,Route
from student.models import Student
from schoolbus.serializers import BusSerializer , RouteSerializer , BusPointSerializer





class StudentBusSerializer(serializers.ModelSerializer):
    
    bus = BusSerializer(read_only=True)
    bus_id = serializers.PrimaryKeyRelatedField(queryset=Bus.objects.all(), source='bus', write_only=True)
    route_id = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all(), write_only=True)
    bus_point_id = serializers.PrimaryKeyRelatedField(queryset=BusPoint.objects.all(), write_only=True)

    class Meta:
        model = Student
        fields = [
            'id', 'user', 'admission_no', 'guardian_name', 'address',
            'classRoom', 'bus', 'bus_id', 'route_id', 'bus_point_id'
        ]
        
class StudentBusGetSerializer(serializers.ModelSerializer):
    bus = BusSerializer()
    
    class Meta:
        model = Student
        fields = ['id', 'user', 'admission_no', 'guardian_name', 'address', 'classRoom', 'bus']


class BusAssignmentSerializer(serializers.Serializer):
    route_number = serializers.IntegerField()
    bus_point_id = serializers.IntegerField()



class StudentBusssSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'user', 'admission_no', 'guardian_name', 'address', 'classRoom', 'bus', 'route', 'bus_point']
        
        
class BusDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = ['id', 'bus_no', 'driver_name', 'plate_number', 'capacity']

class RouteDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id', 'route_no', 'from_location', 'to_location']

class BusPointDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusPoint
        fields = ['id', 'name', 'fee']

class StudentSerializer(serializers.ModelSerializer):
    bus = BusDetailSerializer()
    route = RouteDetailSerializer()
    bus_point = BusPointDetailSerializer()

    class Meta:
        model = Student
        fields = ['id', 'user', 'admission_no', 'guardian_name', 'address', 'classRoom', 'bus', 'route', 'bus_point']