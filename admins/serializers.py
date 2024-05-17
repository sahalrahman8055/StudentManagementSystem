from rest_framework import serializers
from admins.models import User , Role
from teacher.models import ClassRoom , Teacher , ClassRoomTeacher
from student.models import Student


class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'username','gender', 'phone', 'email', 'role']
        
    def create(self, validated_data):
        role, _ = Role.objects.get_or_create(name='teacher')
        validated_data['role'] = role
        return super().create(validated_data)
    
class TeacherPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'pen_no', 'short']
        extra_kwargs = {'password': {'write_only': True}}


class TeacherChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['pen_no', 'short']

class TeacherListSerializer(serializers.ModelSerializer):
    teacher = TeacherChoiceSerializer()
    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'phone', 'email','teacher']
        
        
class TeacherGetUpdateSerializer(serializers.ModelSerializer):
    teacher = TeacherChoiceSerializer()
    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'phone', 'email','teacher']
        
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)

        teacher_data = validated_data.pop('teacher', None)
        if teacher_data:
            teacher_instance, _ = Teacher.objects.get_or_create(user=instance)
            for attr, value in teacher_data.items():
                setattr(teacher_instance, attr, value)
            teacher_instance.save()

        instance.save()
        return instance

    
    

        


class UserStudentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'name', 'username','phone','gender', 'role','date_of_birth']
        extra_kwargs = {
            'email': {'write_only': True, 'required': False}  # Exclude email from validation and creation
        }
        
        
    def create(self,validated_data):
        role, _ = Role.objects.get_or_create(name='student')
        validated_data['role'] = role
        return super().create(validated_data)


class StudentSerializer(serializers.ModelSerializer):
    pincode = serializers.CharField(max_length=10, required=True)
    house_name = serializers.CharField(max_length=150, required=True)
    post_office = serializers.CharField(max_length=150, required=True)
    place = serializers.CharField(max_length=100,required=True)

    class Meta:
        model = Student
        fields = ['id', 'admission_no', 'guardian_name', 'address', 'pincode', 'house_name', 'post_office','place','classRoom']
        
    def create(self, validated_data):
        # Extracting individual fields from the address
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
        
        student = Student.objects.create(address=address, **validated_data)
        
        return student


class StudentChoiceSerializer(serializers.ModelSerializer):
    # pincode = serializers.CharField(max_length=10, required=True)
    # house_name = serializers.CharField(max_length=150, required=True)
    # post_office = serializers.CharField(max_length=150, required=True)
    # place = serializers.CharField(max_length=100, required=True)
    
    class Meta:
        model = Student
        fields = ['id', 'admission_no', 'guardian_name', 'address']
        # , 'pincode', 'house_name', 'post_office','place']

    
    
class StudentListSerializer(serializers.ModelSerializer):
    student = StudentChoiceSerializer()
    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'phone','gender', 'role','date_of_birth','student']
        
        
class StudentGetUpdateSerializer(serializers.ModelSerializer):
    student = StudentChoiceSerializer()

    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'phone', 'gender', 'date_of_birth', 'student']
        
    def update(self, instance, validated_data):
        # Update user related fields
        instance.name = validated_data.get('name', instance.name)
        instance.username = validated_data.get('username', instance.username)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        
        student_data = validated_data.pop('student', None)
        if student_data:
            # Update student related fields
            instance.student.admission_no = student_data.get('admission_no', instance.student.admission_no)
            instance.student.guardian_name = student_data.get('guardian_name', instance.student.guardian_name)
            instance.student.save()
            
            # # Update address field
            # pincode = student_data.get('pincode', instance.student.pincode)
            # house_name = student_data.get('house_name', instance.student.house_name)
            # post_office = student_data.get('post_office', instance.student.post_office)
            # place = student_data.get('place', instance.student.place)
            
            # address_parts = [part for part in [house_name, post_office, pincode, place] if part]
            # instance.address = ", ".join(address_parts)

        instance.save()
        return instance

class ClassRoomStudentsListSerializer(serializers.ModelSerializer):
    user = UserStudentSerializer()
    
    class Meta:
        model = Student
        fields = ['id', 'admission_no', 'guardian_name', 'address','user']
        
        
class ClassRoomTeacherChoiceSerializer(serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField()
    class Meta:
        model = ClassRoomTeacher
        fields = ('teacher',)

    def get_teacher(self, obj):
        return obj.teacher.user.name
    
    
class ClassRoomSerializer(serializers.ModelSerializer):
    students = ClassRoomStudentsListSerializer(many=True, read_only=True)
    classTeacher = serializers.SerializerMethodField()

    class Meta:
        model = ClassRoom
        fields = ('id', 'name', 'capacity', 'classTeacher', 'students')

    def get_classTeacher(self, obj):
        class_teacher = obj.classroom_teachers.filter(is_class_teacher=True).first()
        print(ClassRoomTeacherChoiceSerializer(class_teacher).data)
        if class_teacher:
            return ClassRoomTeacherChoiceSerializer(class_teacher).data
        return None
        
        
class ClassTeacherSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ClassRoomTeacher
        fields = ('teacher','classroom','is_class_teacher')