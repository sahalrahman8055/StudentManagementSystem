from rest_framework import serializers
from schoolbus.models import Bus,BusPoint,Route
from student.models import Student , StudentBusService
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

class StudentBusServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentBusService
        fields = ['bus', 'route', 'bus_point', 'annual_fees']


class StudentBusSerializer(serializers.ModelSerializer):
    bus_service = StudentBusServiceSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'user', 'admission_no', 'guardian_name', 'address','is_bus', 'classRoom', 'bus_service']

        
        
        
class FilteredBusPointListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        request = self.context['request']
        search_query = request.query_params.get('query', '').lower()
        filtered_data = data.filter(name__icontains=search_query)
        return super().to_representation(filtered_data)



class FilteredBusPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusPoint
        list_serializer_class = FilteredBusPointListSerializer
        fields = ['id', 'name', 'fee', 'route']
        
        
        
class RouteListSerializer(serializers.ModelSerializer):
    bus_points = FilteredBusPointSerializer(many=True, read_only=True, context={'request': None})

    class Meta:
        model = Route
        fields = ['id', 'route_no', 'from_location', 'to_location', 'bus', 'bus_points']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'user', 'admission_no', 'guardian_name', 'address', 'classRoom']



class StudentBusServiceSerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = StudentBusService
        fields = ['student', 'bus', 'route', 'bus_point', 'annual_fees']

class StudentByRouteSerializer(serializers.ModelSerializer):
    bus = BusSerializer()
    students = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = ['id', 'route_no', 'from_location', 'to_location', 'bus_points', 'bus', 'students']

    def get_students(self, obj):
        bus_services = StudentBusService.objects.filter(route=obj)
        return StudentBusServiceSerializer(bus_services, many=True).data