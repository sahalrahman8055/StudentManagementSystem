from rest_framework import serializers
from admins.models import User , Role
from teacher.models import ClassRoom , Teacher
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

    
    

class ClassRoomSerializer(serializers.ModelSerializer):
   
   class Meta: 
        model = ClassRoom
        fields = ('name','capacity')
        


class UserStudentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'phone','gender', 'role','date_of_birth']
        
        
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
        fields = ['id', 'admission_no', 'guardian_name', 'address', 'pincode', 'house_name', 'post_office','place']
        
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
                #   , 'pincode', 'house_name', 'post_office','place']

    
    
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
            student_instance, _ = Student.objects.get_or_create(user=instance)
            for attr, value in student_data.items():
                setattr(student_instance, attr, value)
            student_instance.save()

        instance.save()
        return instance



#   def update(self, instance, validated_data):
        
#         student_data = validated_data.pop('student', None)

#         if student_data:
#             # Access address fields from student_data
#             pincode = student_data.pop('pincode', None)
#             house_name = student_data.pop('house_name', None)
#             post_office = student_data.pop('post_office', None)
#             place = student_data.pop('place', None)

#             # Update student related fields
#             student_serializer = self.fields['student']
#             student_instance = instance.student
#             student_serializer.update(student_instance, student_data)
        
#         instance.name = validated_data.get('name', instance.name)
#         instance.phone = validated_data.get('phone', instance.phone)
#         instance.gender = validated_data.get('gender', instance.gender)
#         instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        
#         student_data = validated_data.pop('student', None)
#         if student_data:
#             teacher_instance, _ = Teacher.objects.get_or_create(user=instance)
#             for attr, value in student_data.items():
#                 setattr(teacher_instance, attr, value)
#             teacher_instance.save()

#         if pincode:
#             instance.address += f"{pincode}"
#         if house_name:
#             instance.address += f", {house_name}"
#         if post_office:
#             instance.address += f",{post_office}"
#         if place:
#             instance.place += f",{place}"
        
#         instance.save()
#         return instance





# student_data = validated_data.pop('student', None)

#         if student_data:
#             # Access address fields from student_data
#             pincode = student_data.pop('pincode', None)
#             house_name = student_data.pop('house_name', None)
#             post_office = student_data.pop('post_office', None)
#             place = student_data.pop('place', None)

 # Update student related fields
            # student_serializer = self.fields['student']
            # student_instance = instance.student
            # student_serializer.update(student_instance, student_data)