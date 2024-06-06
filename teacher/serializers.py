from rest_framework import serializers
from schoolbus.models import Bus , BusPoint , Route
from rest_framework import serializers
from admins.models import User
from student.models import Student , StudentBusService
from teacher.models import ClassRoom , Teacher 
# from admins.serializers import UserSerializer

class TeacherLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()




class BusPointChoiceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BusPoint
        fields = ['id','route','name','fee']
    
class RouteChoiceSerializer(serializers.ModelSerializer):
    bus_points = BusPointChoiceSerializer(many=True,read_only=True)
    
    class Meta:
        model = Route
        fields = ['id','bus','route_no','from_location','to_location','bus_points']
           
    
class BusListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Bus
        fields = ['id','bus_no','driver_name','plate_number','capacity']
    
        
class StudentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name','gender']

class UserStudentSerializer(serializers.ModelSerializer):
    user = StudentListSerializer(read_only=True)
    
    class Meta:
        model = Student
        fields =  ['id', 'admission_no','user']   



class StudentSerializer(serializers.ModelSerializer):
    user = StudentListSerializer()
    class Meta:
        model = Student
        fields = ('admission_no','user','classRoom')
        read_only_fields = ('admission_no',)
        
        

class BusStudentSerializer(serializers.ModelSerializer):
    student = UserStudentSerializer()
    bus = BusListSerializer()
    route = RouteChoiceSerializer()
    bus_point = BusPointChoiceSerializer()

    class Meta:
        model = StudentBusService
        fields = ['student', 'bus','route', 'bus_point', 'annual_fees']
        