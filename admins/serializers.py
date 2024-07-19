from rest_framework import serializers
from admins.models import User
from teacher.models import ClassRoom, Teacher, ClassRoomTeacher
from student.models import Student
from django.contrib.auth.models import Group
import random
import string
import cloudinary.uploader
import re
 

class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


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
        user_data = validated_data.pop("user",None)
        photo = validated_data.pop("photo", None)

        if user_data:
            user = instance.user
            user.email = user_data.get("email", user.email)
            user.username = user_data.get("username", user.username)
            user.phone = user_data.get("phone", user.phone)
            user.gender = user_data.get("gender", user.gender)
            user.save()

        instance.save()

        return instance


class UserStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "username", 'gender',"phone", "date_of_birth"]
        extra_kwargs = {
            "email": {
                "write_only": True,
                "required": False,
            }  # Exclude email from validation and creation
        }


class StudentSerializer(serializers.ModelSerializer):
    pincode = serializers.CharField(max_length=10, write_only=True)
    house_name = serializers.CharField(max_length=150, write_only=True)
    post_office = serializers.CharField(max_length=150, write_only=True)
    place = serializers.CharField(max_length=100, write_only=True)
    user = UserStudentSerializer()

    class Meta:
        model = Student
        fields = [
            "id",
            "admission_no",
            "guardian_name",
            "address",
            "pincode",
            "house_name",
            "post_office",
            "place",    
            "classRoom",
            "user",
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        username = user_data.get("username")
        admission_no = validated_data.get("admission_no")

        # Check if user with the same username already exists
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {"username": f"The username '{username}' is already taken."}
            )

        # Check if student with the same admission number already exists
        if Student.objects.filter(admission_no=admission_no).exists():
            raise serializers.ValidationError(
                {"admission_no": f"The admission number '{admission_no}' is already taken."}
            )

        # Create the user instance
        user = User.objects.create_user(**user_data)

        # Create the address string
        address = self.construct_address(
            validated_data.pop("house_name", None),
            validated_data.pop("post_office", None),
            validated_data.pop("pincode", None),
            validated_data.pop("place", None),
        )

        # Create the student instance
        student = Student.objects.create(user=user, address=address, **validated_data)

        # Add the student to the 'student' group
        student_group = Group.objects.get(name="student")
        student_group.user_set.add(user) 

        return student

    def construct_address(
        self, house_name: str, post_office: str, pincode: str, place: str
    ) -> str:
        """
        Construct the address from individual components.
        """
        address_parts = filter(None, [house_name, post_office, pincode, place])
        return ", ".join(address_parts)

    def validate(self, data):
        """
        Validate the incoming data.
        """
        user_data = data.get("user")
        username = user_data.get("username")
        admission_no = data.get("admission_no")

        # Check if user with the same username already exists
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {"username": f"The username '{username}' is already taken."}
            )

        # Check if student with the same admission number already exists
        if Student.objects.filter(admission_no=admission_no).exists():
            raise serializers.ValidationError(
                {"admission_no": f"The admission number '{admission_no}' is already taken."}
            )

        return data

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
    
    # def validate(self, data):
    #     # Normalize the value
    #     normalized_value = re.sub(r'\s+', '', data['name']).lower()
    #     # Check if the normalized name exists in the database
    #     if ClassRoom.objects.filter(name=normalized_value).exists():
    #         raise serializers.ValidationError({'name': f'{data["name"]} is already taken. Please choose a different class name.'})
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

    def to_internal_value(self, data):
        if isinstance(data, str):
            data = {'name': data}
        return super().to_internal_value(data)

    def create(self, validated_data):
        class_room, created = ClassRoom.objects.get_or_create(**validated_data)
        return class_room


def generate_username(name):
        return ''.join(name.split()) + ''.join(random.choices(string.digits, k=2))

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
            "address",
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
        
        if 'username' not in user_data or not user_data['username']:
            name = user_data.get('name', '')
            username = generate_username(name)  
            user_data['username'] = username

        user = User.objects.create_user(**user_data)
        class_room, _ = ClassRoom.objects.get_or_create(**class_room_data)

        address = self.construct_address(
            validated_data.pop("house_name", ""),
            validated_data.pop("post_office", ""),
            validated_data.pop("pincode", ""),
            validated_data.pop("place", "")
        )

        student = Student.objects.create(
            user=user,
            classRoom=class_room,
            address=address,
            **validated_data
        )

        student_group, _ = Group.objects.get_or_create(name="student")
        student_group.user_set.add(user) 

        return student
    
    def construct_address(self, house_name, post_office, pincode, place):
        return ", ".join(filter(None, [house_name, post_office, pincode, place]))

    def validate(self, data):
        user_data = data.get("user")
        username = user_data.get("username")
        admission_no = data.get("admission_no")

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {"user.username": f"The username '{username}' is already taken."}
            )

        if Student.objects.filter(admission_no=admission_no).exists():
            raise serializers.ValidationError(
                {"admission_no": f"The admission number '{admission_no}' is already taken."}
            )

        return data



class ClassTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id','user','classRoom')