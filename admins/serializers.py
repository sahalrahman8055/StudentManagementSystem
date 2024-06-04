from rest_framework import serializers
from admins.models import User
from teacher.models import ClassRoom , Teacher , ClassRoomTeacher
from student.models import Student
from django.contrib.auth.models import Group

class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):  
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'username', 'phone', 'gender','is_staff']
        extra_kwargs = {'password': {'write_only': True}}

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = ['user', 'pen_no']
        
    def validate(self, data):

        user_data = data.get('user')
        username = user_data.get('username')
        pen_no = data.get('pen_no')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": f"The username '{username}' is already taken."})

        if Teacher.objects.filter(pen_no=pen_no).exists():
            raise serializers.ValidationError({"pen_no": f"The pen number '{pen_no}' is already taken."})

        return data
    
    

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['is_staff'] = True  
        user = User.objects.create_user(**user_data)
        
        teacher = Teacher.objects.create(user=user, pen_no=validated_data['pen_no'])

        teacher_group = Group.objects.get(name='teacher')
        user.groups.add(teacher_group)

        return teacher
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        
        user = instance.user
        user.email = user_data.get('email', user.email)
        user.name = user_data.get('name', user.name)
        user.phone = user_data.get('phone', user.phone)
        user.gender = user_data.get('gender', user.gender)
        user.date_of_birth = user_data.get('date_of_birth', user.date_of_birth)
        user.save()

        instance.save()

        return instance

   
        
# class TeacherGetUpdateSerializer(serializers.ModelSerializer):
#     teacher = TeacherChoiceSerializer()
#     class Meta:
#         model = User
#         fields = ['id', 'name', 'username', 'phone', 'email','is_active','teacher']
        
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.phone = validated_data.get('phone', instance.phone)
#         instance.email = validated_data.get('email', instance.email)
#         instance.is_active = validated_data.get('is_active', instance.is_active)

#         teacher_data = validated_data.pop('teacher', None)
#         if teacher_data:
#             teacher_instance, _ = Teacher.objects.get_or_create(user=instance)
#             for attr, value in teacher_data.items():
#                 setattr(teacher_instance, attr, value)
#             teacher_instance.save()

#         instance.save()
#         return instance

    

class UserStudentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'name', 'username','phone','gender','date_of_birth']
        extra_kwargs = {
            'email': {'write_only': True, 'required': False}  # Exclude email from validation and creation
        }
        


class StudentSerializer(serializers.ModelSerializer):
    pincode = serializers.CharField(max_length=10, required=True)
    house_name = serializers.CharField(max_length=150, required=True)
    post_office = serializers.CharField(max_length=150, required=True)
    place = serializers.CharField(max_length=100,required=True)
    user = UserStudentSerializer()

    class Meta:
        model = Student
        fields = ['id', 'admission_no', 'guardian_name', 'address', 'pincode', 'house_name', 'post_office','place','classRoom','user']
        
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        
        user = User.objects.create_user(**user_data)

        pincode = validated_data.pop('pincode', None)
        house_name = validated_data.pop('house_name', None)
        post_office = validated_data.pop('post_office', None)
        place = validated_data.pop('place', None)
        
        address = ""
        if house_name:
            address += f" {house_name}"
        if post_office:
            address += f", {post_office}"
        if pincode:
            address += f",  {pincode}"
        if place:
            address += f", {place}"
        
        student = Student.objects.create(user=user , address=address, **validated_data)
        
        student_group = Group.objects.get(name='student')
        user.groups.add(student_group)
        
        return student
    
    def validate(self, data):

        user_data = data.get('user')
        username = user_data.get('username')
        admission_no = data.get('admission_no')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": f"The username '{username}' is already taken."})
        
        if Student.objects.filter(admission_no=admission_no).exists():
            raise serializers.ValidationError({"username": f"The username '{username}' is already taken."})

        return data


# class StudentChoiceSerializer(serializers.ModelSerializer):
#     # pincode = serializers.CharField(max_length=10, required=True)
#     # house_name = serializers.CharField(max_length=150, required=True)
#     # post_office = serializers.CharField(max_length=150, required=True)
#     # place = serializers.CharField(max_length=100, required=True)
    
#     class Meta:
#         model = Student
#         fields = ['id', 'admission_no', 'guardian_name', 'address','classRoom']
#         # , 'pincode', 'house_name', 'post_office','place']

    
    
  
        
class ClassRoomTeacherChoiceSerializer(serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField()
    class Meta:
        model = ClassRoomTeacher
        fields = ('teacher',)

    def get_teacher(self, obj):
        return obj.teacher.user.name
    
    
# class ClassRoomSerializer(serializers.ModelSerializer):
#     students = ClassRoomStudentsListSerializer(many=True, read_only=True)
#     classTeacher = serializers.SerializerMethodField()

#     class Meta:
#         model = ClassRoom
#         fields = ('id', 'name', 'capacity', 'classTeacher', 'students')

#     def get_classTeacher(self, obj):
#         class_teacher = obj.classroom_teachers.filter(is_class_teacher=True).first()
#         print(ClassRoomTeacherChoiceSerializer(class_teacher).data)
#         if class_teacher:
#             return ClassRoomTeacherChoiceSerializer(class_teacher).data
#         return None
        
        
class ClassTeacherSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ClassRoomTeacher
        fields = ('teacher','classroom','is_class_teacher')