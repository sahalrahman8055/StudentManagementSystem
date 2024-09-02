from rest_framework import serializers
from admins.models import User
from teacher.models import ClassRoom, Teacher, ClassRoomTeacher
from student.models import Student
from django.contrib.auth.models import Group
import random
import string
import re
 

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        ref_name = 'AuthUser'
        read_only_fields = ('id', 'email')
        extra_kwargs = {'password': {'write_only': True}}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "username", "phone", "gender", "is_staff"]
        extra_kwargs = {"password": {"write_only": True}}


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = ["id","user", "pen_no",'photo']

    def validate(self, data):
        user_data = data.get("user")
        username = user_data.get("username") if user_data else None
        pen_no = data.get("pen_no")

        if username and User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {"username": f"The username '{username}' is already taken."}
            )

        if Teacher.objects.filter(pen_no=pen_no).exists():
            raise serializers.ValidationError(
                {"pen_no": f"The pen number '{pen_no}' is already taken."}
            )

        return data

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data["is_staff"] = True

        user = User.objects.create_user(**user_data)

        teacher = Teacher.objects.create(
            user=user,
            pen_no=validated_data["pen_no"],
        )
        teacher_group, _ = Group.objects.get_or_create(name="teacher")
        teacher_group.user_set.add(user)

        return teacher

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)

        if user_data:
            user = instance.user
            user.email = user_data.get("email", user.email)
            user.username = user_data.get("username", user.username)
            user.phone = user_data.get("phone", user.phone)
            user.gender = user_data.get("gender", user.gender)
            user.save()

        # Update Teacher model fields
        instance.pen_no = validated_data.get("pen_no", instance.pen_no)
        instance.photo = validated_data.get("photo", instance.photo)  # If needed
        instance.save()

        return instance



class UserStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", 'gender',"phone", "date_of_birth"]
        extra_kwargs = {
            "email": {
                "write_only": True,
                "required": False,
            }  # Exclude email from validation and creation
        }


class StudentSerializer(serializers.ModelSerializer):
    user = UserStudentSerializer()

    class Meta:
        model = Student
        fields = [
            "id",
            "admission_no",
            "photo",
            "guardian_name",
            "pincode",
            "house_name",
            "post_office",
            "place",    
            "classRoom",
            "user",
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        # username = user_data.get("username")
        admission_no = validated_data.get("admission_no")

        # Check if user with the same username already exists
        # if User.objects.filter(username=username).exists():
        #     raise serializers.ValidationError(
        #         {"username": f"The username '{username}' is already taken."}
        #     )

        # Check if student with the same admission number already exists
        if Student.objects.filter(admission_no=admission_no).exists():
            raise serializers.ValidationError(
                {"admission_no": f"The admission number '{admission_no}' is already taken."}
            )

        user = User.objects.create_user(**user_data)

        student = Student.objects.create(user=user, **validated_data)

        student_group = Group.objects.get(name="student")
        student_group.user_set.add(user) 

        return student



    # def validate(self, data):
    #     """
    #     Validate the incoming data.
    #     """
    #     user_data = data.get("user")
    #     username = user_data.get("username")
    #     admission_no = data.get("admission_no")

    #     if User.objects.filter(username=username).exists():
    #         raise serializers.ValidationError(
    #             {"username": f"The username '{username}' is already taken."}
    #         )

    #     if Student.objects.filter(admission_no=admission_no).exists():
    #         raise serializers.ValidationError(
    #             {"admission_no": f"The admission number '{admission_no}' is already taken."}
    #         )

    #     return data

class ClassRoomTeacherChoiceSerializer(serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField()

    class Meta:
        model = ClassRoomTeacher
        fields = ("teacher",)

    def get_teacher(self, obj):
        return obj.teacher.user.name


class ClassRoomSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)
    classTeacher = serializers.SerializerMethodField()

    class Meta:
        model = ClassRoom
        fields = ('id', 'name', 'capacity', 'classTeacher', 'students')

    def get_classTeacher(self, obj):
        class_teacher = obj.classroom_teachers.filter(is_class_teacher=True).first()
        if class_teacher:
            return ClassRoomTeacherChoiceSerializer(class_teacher).data
        return None
    
    # def validate_division(self, value):
    #     value = value.strip().upper()
    #     if not value.isalpha() or len(value) != 1:
    #         raise serializers.ValidationError("Division must be a single uppercase letter from A to Z.")
    #     return value


    # def validate(self, data):
    #     name = data.get('name')
    #     division = data.get('division')

    #     # Check for existing classrooms with the same name and division
    #     if ClassRoom.objects.filter(name=name, division=division).exclude(id=self.instance.id if self.instance else None).exists():
    #         raise serializers.ValidationError({"non_field_errors": ["A classroom with this name and division already exists."]})
        
    #     return data
    


class ClassTeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClassRoomTeacher
        fields = ("teacher", "classroom", "is_class_teacher")


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    
    

class ClassSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = ClassRoom
        fields = ['id', 'name']


class StudentUploadSerializer(serializers.ModelSerializer):
    pincode = serializers.CharField(max_length=10, write_only=True)
    house_name = serializers.CharField(max_length=150, write_only=True)
    post_office = serializers.CharField(max_length=150, write_only=True)
    place = serializers.CharField(max_length=100, write_only=True)
    classRoom = ClassSerializer()
    user = UserStudentSerializer()

    class Meta:
        model = Student
        fields = [
            "id",
            "admission_no",
            "guardian_name",
            "pincode",
            "house_name",
            "post_office",
            "place",
            "classRoom",
            "user",
        ]
        

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        class_room_data = validated_data.pop("classRoom")

        user = User.objects.create_user(**user_data)
        class_room, _ = ClassRoom.objects.get_or_create(**class_room_data)

        student = Student.objects.create(
            user=user,
            classRoom=class_room,
            **validated_data
        )

        student_group, _ = Group.objects.get_or_create(name="student")
        student_group.user_set.add(user) 

        return student

    def validate(self, data):
        admission_no = data.get("admission_no")

        if Student.objects.filter(admission_no=admission_no).exists():
            raise serializers.ValidationError(
                {"admission_no": f"The admission number '{admission_no}' is already taken."}
            )

        return data



class ClassTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id','user','classRoom')