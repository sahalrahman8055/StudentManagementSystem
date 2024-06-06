from rest_framework import serializers
from admins.models import User
from student.models import Student , StudentBusService
from teacher.models import ClassRoom , Teacher 
# from admins.serializers import UserSerializer
from student.serializers import BusSerializer , RouteSerializer , BusPointSerializer
class TeacherLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()





# class StudentSerializer(serializers.ModelSerializer):
#     user = StudentListSerializer()
#     class Meta:
#         model = Student
#         fields = ['id', 'user', 'admission_no', 'classRoom']

# class ClassRoomGetSerializer(serializers.ModelSerializer):
#     students = StudentSerializer(many=True, read_only=True)

#     class Meta:
#         model = ClassRoom
#         fields = ['id', 'name', 'capacity', 'students']


# class ClassStudentsBusSerializer(serializers.ModelSerializer):
#     user = StudentListSerializer()
#     bus_service = BusSerializer()
    
#     class Meta:
#         model = Student
#         fields = ['id', 'user', 'admission_no', 'guardian_name', 'address', 'classRoom', 'is_bus', 'bus_service']
        
class UserStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name','gender']


class BusStudentSerializer(serializers.ModelSerializer):
    student = UserStudentSerializer()
    bus = BusSerializer()
    route = RouteSerializer()
    bus_point = BusPointSerializer()

    class Meta:
        model = StudentBusService
        fields = ['student', 'bus', 'route', 'bus_point', 'annual_fees']


class StudentSerializer(serializers.ModelSerializer):
    user = UserStudentSerializer()
    class Meta:
        model = Student
        fields = ('admission_no','user','classRoom')
        read_only_fields = ('admission_no',)
        
        
