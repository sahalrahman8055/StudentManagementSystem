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


class StudentBusssSerializer(serializers.ModelSerializer):
    bus_service = StudentBusServiceSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'user', 'admission_no', 'guardian_name', 'address', 'classRoom', 'bus_service']

        
        
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
        

class BusPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusPoint
        fields = ['id', 'name', 'fee', 'route']
        
        
        
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
        
        
        
class RouteSerializer(serializers.ModelSerializer):
    bus_points = FilteredBusPointSerializer(many=True, read_only=True, context={'request': None})

    class Meta:
        model = Route
        fields = ['id', 'route_no', 'from_location', 'to_location', 'bus', 'bus_points']
