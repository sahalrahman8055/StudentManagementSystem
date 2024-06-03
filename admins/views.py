from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import (
     AdminLoginSerializer , 
     TeacherSerializer,
    #  ClassRoomSerializer,
    #  UserSerializer,
     StudentSerializer,
    #  UserStudentSerializer,
    #  TeacherListSerializer,
    #  TeacherGetUpdateSerializer,
    #  StudentListSerializer,
    #  ClassTeacherSerializer,
    #  StudentGetUpdateSerializer,
)
from rest_framework.views import APIView 
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from admins.utilities.token import get_tokens_for_user
from admins.models import User 
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from teacher.models import ClassRoom , Teacher ,ClassRoomTeacher
from student.models import Student
from django.core.mail import send_mail
from django.conf import settings
from .utilities.utils import send_teacher_email
from rest_framework.permissions import IsAuthenticated
from admins.utilities.permission import IsAdminUser
from rest_framework.generics import CreateAPIView

class AdminLoginAPIView(APIView):
    def post(self, request):
      serializer = AdminLoginSerializer(data=request.data)
      if serializer.is_valid():
          username = serializer.validated_data['username']
          password = serializer.validated_data['password']
          user = authenticate( username=username, password=password)

          if user is not None:
            login(request, user)
            token = get_tokens_for_user(user)
            return Response({'message': 'Login successful', 'token':token}, status=status.HTTP_200_OK)
          return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
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
            return Response({"error": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    


            
#             pen_no = teacher_instance.pen_no
#             username = user_instance.username
#             user_instance.set_password(pen_no)
#             user_instance.save()

#             send_teacher_email(user_instance, username, pen_no)

        
        
# class TeacherGetUpdateViewset(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = TeacherGetUpdateSerializer
#     permission_classes = [IsAuthenticated]
    
    
#     def retrieve(self, request, *args, **kwargs):
#         try:
#             teacher_id = kwargs.get('pk')
#             teacher = User.objects.get(id=teacher_id , role__name__icontains='teacher')
#             serializer = self.get_serializer(teacher)
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             return Response({"error":"Teacher not found"},status=status.HTTP_404_NOT_FOUND)
        
        
#     def update(self, request, *args, **kwargs):
#         try:
#             instance = self.get_object()
#             print(instance)
#             serializer = self.get_serializer(instance, data=request.data, partial=True)
#             serializer.is_valid(raise_exception=True)
#             self.perform_update(serializer)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
    

class StudentListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        student = User.objects.filter(role__name__icontains='student')
        serializer = StudentListSerializer(student, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        user_serializer = UserStudentSerializer(data=request.data)
        student_serializer = StudentSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True) and (
            student_serializer.is_valid(raise_exception=True)
        ):
            user_instance = user_serializer.save()
            
            classroom_id = request.GET.get('q')
            try:
                classroom = ClassRoom.objects.get(id=classroom_id)
            except ClassRoom.DoesNotExist:
                return Response({"msg":"classroom does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
            student_serializer.save(user=user_instance, classRoom=classroom)
            
            return Response(
                {"message": "Student created successfully"}, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": "Error creating teacher"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
            
            
# class StudentGetUpdateViewset(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = StudentGetUpdateSerializer
#     permission_classes = [IsAuthenticated]
    
    
    def retrieve(self, request, *args, **kwargs):
        try:
            student_id = kwargs.get('pk')
            student = User.objects.get(id=student_id, role__name__icontains='student')
            serializer = self.get_serializer(student)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except:
            return Response({"error":"Student not found"},status=status.HTTP_404_NOT_FOUND)
        
        
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

            
# class ClassRoomViewset(viewsets.ModelViewSet):
#     queryset = ClassRoom.objects.all()
#     serializer_class = ClassRoomSerializer
#     permission_classes = [IsAuthenticated]




# class ClassTeacherViewset(viewsets.ModelViewSet):
#     queryset = ClassRoomTeacher.objects.all()
#     serializer_class = ClassTeacherSerializer
#     permission_classes = [IsAuthenticated]
    
#     def create(self, request, *args, **kwargs):
#         Q_Base = request.GET.get('q')
#         if Q_Base:
#             try:
#                 classroom = ClassRoom.objects.get(id=Q_Base)
#             except ClassRoom.DoesNotExist:
#                 return Response({"msg":"Classroom not exist"},status=status.HTTP_404_NOT_FOUND)
            
#             teacher_id = request.data.get('teacher_id')
            
#             if teacher_id:
#                 try:
#                     teacher = Teacher.objects.get(user_id=teacher_id)
#                 except Teacher.DoesNotExist:
#                     return Response({"msg": "Teacher does not exist"}, status=status.HTTP_404_NOT_FOUND)
                
#                 class_teacher, _ = ClassRoomTeacher.objects.get_or_create(
#                     teacher=teacher,
#                     classroom=classroom,
#                 )
                
#                 class_teacher.is_class_teacher = True
#                 class_teacher.save()
                
#                 return Response({"msg": "Class teacher assigned successfully"}, status=status.HTTP_201_CREATED)
#             else:
#                 return Response({"msg": "Teacher ID not provided in the request"}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({"msg": "Classroom ID not provided in the request"}, status=status.HTTP_400_BAD_REQUEST)