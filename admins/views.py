from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import (
    AdminLoginSerializer,
    TeacherSerializer,
    ClassRoomSerializer,
    StudentSerializer,
    ClassTransferSerializer,
    ClassTeacherSerializer,
    FileUploadSerializer,
    StudentUploadSerializer
)
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from admins.utilities.token import get_tokens_for_user
from admins.models import User
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from teacher.models import ClassRoom, Teacher, ClassRoomTeacher
from student.models import Student
from rest_framework.permissions import IsAuthenticated, AllowAny
from admins.utilities.permission import IsAdminUser
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import action
import openpyxl


class AdminLoginAPIView(APIView):
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        print(request.data)
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                token = get_tokens_for_user(user)
                return Response(
                    {"message": "Login successful", "token": token},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = TeacherSerializer

    def update(self, request, *args, **kwargs):
        try:
            teacher = self.get_object()
            serializer = self.get_serializer(teacher, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Teacher.DoesNotExist:
            return Response(
                {"error": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    permission_classes = [IsAdminUser]  
    serializer_class = StudentSerializer

    def perform_create(self, serializer):
        classroom_id = self.request.query_params.get("classroom_id")
        if not classroom_id:
            raise serializer.ValidationError(
                {"classroom_id": "This query parameter is required."}
            )
        try:
            classroom = ClassRoom.objects.get(id=classroom_id)
        except ClassRoom.DoesNotExist:
            raise serializer.ValidationError({"classroom_id": "Invalid classroom ID."})

        serializer.save(classRoom=classroom)
        return Response("Student Created Successfully",status=status.HTTP_201_CREATED)
    
    
    @action(detail=True, methods=['post'])
    def transfer(self, request,pk=None):
        print(request.data)
        student = self.get_object()
        classroom_id = request.data.get('classRoom')
        print(classroom_id)
        
        if not classroom_id:
            return Response({"error": "ClassRoom ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            new_classroom = ClassRoom.objects.get(pk=classroom_id)
            print(new_classroom)
        except ClassRoom.DoesNotExist:
            return Response({"error": "ClassRoom not found"}, status=status.HTTP_404_NOT_FOUND)
        
        student.classRoom = new_classroom
        student.save()
        
        return Response(
            {
                "message": "Class transfer successful",
                "student": self.get_serializer(student).data
            },
            status=status.HTTP_201_CREATED
        )




class ClassRoomViewset(viewsets.ModelViewSet):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        grade = self.request.query_params.get('grade')
        if grade is not None:
            queryset = queryset.filter(name__icontains=grade)
        return queryset




class ClassTeacherViewset(viewsets.ModelViewSet):
    queryset = ClassRoomTeacher.objects.all()
    serializer_class = ClassTeacherSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        Q_Base = request.GET.get("q")
        if Q_Base:
            try:
                classroom = ClassRoom.objects.get(id=Q_Base)
            except ClassRoom.DoesNotExist:
                return Response(
                    {"msg": "Classroom not exist"}, status=status.HTTP_404_NOT_FOUND
                )

            teacher_id = request.data.get("teacher_id")

            if teacher_id:
                try:
                    teacher = Teacher.objects.get(user_id=teacher_id)
                except Teacher.DoesNotExist:
                    return Response(
                        {"msg": "Teacher does not exist"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                class_teacher, _ = ClassRoomTeacher.objects.get_or_create(
                    teacher=teacher,
                    classroom=classroom,
                )

                class_teacher.is_class_teacher = True
                class_teacher.save()

                return Response(
                    {"msg": "Class teacher assigned successfully"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"msg": "Teacher ID not provided in the request"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"msg": "Classroom ID not provided in the request"},
                status=status.HTTP_400_BAD_REQUEST,
            )



class StudentsUploadViewset(viewsets.ViewSet):
    queryset = Student.objects.all()
    serializer_class = FileUploadSerializer

    @action(detail=False, methods=['post'], url_path='upload')
    def upload(self, request):
        file_serializer = FileUploadSerializer(data=request.data)
        if not file_serializer.is_valid():
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        file = request.FILES.get('file')
        try:
            workbook = openpyxl.load_workbook(file)
            sheet = workbook.active

            headers = [cell.value for cell in sheet[1]]
            students_data = [dict(zip(headers, row)) for row in sheet.iter_rows(min_row=2, values_only=True)]

            errors = []
            successful_creations = []

            for student_data in students_data:
                mapped_data = {
                    "admission_no": student_data.get("Admission No"),
                    "guardian_name": student_data.get("Guardian Name"),
                    "pincode": student_data.get("Pincode"),
                    "house_name": student_data.get("House Name"),
                    "post_office": student_data.get("Post Office"),
                    "place": student_data.get("Place"),
                    "classRoom": {"name": student_data.get("Class Room")},
                    "user": {
                        "username": student_data.get("Username"),
                        "name": student_data.get("Name"),
                        "email": student_data.get("Email"),
                        "phone": student_data.get("Phone"),
                        "gender": student_data.get("Gender"),
                        "date_of_birth": student_data.get("Date of Birth"),
                    }
                }
                serializer = StudentUploadSerializer(data=mapped_data)
                if serializer.is_valid():
                    serializer.save()
                    successful_creations.append(serializer.data)
                else:
                    errors.append(serializer.errors)

            if errors:
                return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Excel uploaded successfully", "data": successful_creations}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
