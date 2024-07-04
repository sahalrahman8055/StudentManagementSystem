from rest_framework import serializers
from admins.models import User
from teacher.models import ClassRoom, Teacher, ClassRoomTeacher
from student.models import Student
from django.contrib.auth.models import Group


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
        fields = ["user", "pen_no"]

    def validate(self, data):

        user_data = data.get("user")
        username = user_data.get("username")
        pen_no = data.get("pen_no")

        if User.objects.filter(username=username).exists():
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

        teacher = Teacher.objects.create(user=user, pen_no=validated_data["pen_no"])

        teacher_group = Group.objects.get_or_create(name="teacher")
        user.groups.add(teacher_group)

        return teacher

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")

        user = instance.user
        user.email = user_data.get("email", user.email)
        user.name = user_data.get("name", user.name)
        user.phone = user_data.get("phone", user.phone)
        user.gender = user_data.get("gender", user.gender)
        user.date_of_birth = user_data.get("date_of_birth", user.date_of_birth)
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
        fields = ["id", "name", "username", "phone", "gender", "date_of_birth"]
        extra_kwargs = {
            "email": {
                "write_only": True,
                "required": False,
            }  # Exclude email from validation and creation
        }
    
    def create(self, validated_data):
        name = validated_data.get('name', '')

        if 'username' not in validated_data or not validated_data['username']:
            username = ''.join(name.split())
            validated_data['username'] = username

        return super().create(validated_data)

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
        student_group = Group.objects.get_or_create(name="student")
        user.groups.add(student_group)

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


class ClassTeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClassRoomTeacher
        fields = ("teacher", "classroom", "is_class_teacher")


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    
    # def validate_file(self, value):
    #     # Validate that the uploaded file is an Excel file
    #     allowed_extensions = ('.xlsx', '.xls')
    #     if not value.name.endswith(allowed_extensions):
    #         raise serializers.ValidationError("Only Excel files are supported.")
    #     return value
    
    
    


class ClassRoomSerializer(serializers.ModelSerializer):
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



class StudentUploadSerializer(serializers.ModelSerializer):
    pincode = serializers.CharField(max_length=10, write_only=True)
    house_name = serializers.CharField(max_length=150, write_only=True)
    post_office = serializers.CharField(max_length=150, write_only=True)
    place = serializers.CharField(max_length=100, write_only=True)
    user = UserStudentSerializer()
    classRoom = ClassRoomSerializer()

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

        user = User.objects.create_user(**user_data)
        class_room, created = ClassRoom.objects.get_or_create(**class_room_data)

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

        student_group = Group.objects.get_or_create(name="student")
        user.groups.add(student_group)

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

    
    def to_internal_value(self, data):
        # First, validate the nested user data using the UserStudentSerializer
        user_data = data.get('user')
        user_serializer = UserStudentSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)

        # Then, validate the nested classRoom data using the ClassRoomSerializer
        class_room_data = data.get('classRoom')
        class_room_serializer = ClassRoomSerializer(data=class_room_data)
        class_room_serializer.is_valid(raise_exception=True)

        return super().to_internal_value(data)