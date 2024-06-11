from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from teacher.serializers import (
    TeacherLoginSerializer,
    BusStudentSerializer,
    StudentSerializer,
    PaymentSerializer
)
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from admins.utilities.token import get_tokens_for_user
from rest_framework.permissions import IsAuthenticated, AllowAny
import logging
from admins.models import User
from .models import Teacher, ClassRoomTeacher, ClassRoom
from student.models import Student, StudentBusService
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from admins.utilities.permission import isTeacher
from rest_framework.decorators import action
from student.models import Payment

logger = logging.getLogger(__name__)

class TeacherLoginAPIView(APIView):

    def post(self, request):
        serializer = TeacherLoginSerializer(data=request.data)
        try:
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
                else:
                    return Response(
                        {"message": "Invalid credentials"},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"message": "An internal server error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class StudentViewset(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [isTeacher]

    def get_classroom(self, user):
        try:
            classroom_teacher = ClassRoomTeacher.objects.get(
                teacher__user=user, is_class_teacher=True
            )
            return classroom_teacher.classroom
        except ClassRoomTeacher.DoesNotExist:
            return None

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not request.user.is_superuser and request.user.is_staff:
            classroom = self.get_classroom(request.user)
            queryset = queryset.filter(classRoom=classroom)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def get_bus_students(self, request):
        queryset = self.get_queryset()
        if not request.user.is_superuser and request.user.is_staff:
            classroom = self.get_classroom(request.user)
            queryset = queryset.filter(is_bus=True, classRoom=classroom)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response("yoyoyooyo")


class BusStudentsViewset(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = BusStudentSerializer
    permission_classes = [isTeacher]

    def get_student_bus_details(self, user_id):
        try:
            bus_service = StudentBusService.objects.select_related("student__user").get(
                student__user__id=user_id
            )
            return bus_service
        except StudentBusService.DoesNotExist:
            return None

    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        bus_service = self.get_student_bus_details(user_id)
        serializer = self.get_serializer(bus_service)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentViewset(viewsets.ModelViewSet):
    queryset= Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes=[IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response({"message": "Payment done successfully","data":serializer.data}, status=status.HTTP_201_CREATED, headers=headers)
    
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     print(instance,'55555')
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data,status=status.HTTP_200_OK)
    
    # @action(detail=False, methods=["GET"])
    def get_user_payments(self, request, user_id):
        payments = Payment.objects.filter(student__user__id=user_id)
        
        serializer = self.get_serializer(payments, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

