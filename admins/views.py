from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import (
     AdminLoginSerializer , 
     TeacherPostSerializer,
     ClassRoomSerializer,
     UserSerializer,
     StudentSerializer,
     UserStudentSerializer,
     TeacherListSerializer,
     TeacherGetUpdateSerializer,
     StudentListSerializer,
     StudentGetUpdateSerializer
)
from rest_framework.views import APIView 
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from admins.utilities.token import get_tokens_for_user
from admins.models import User , Role
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from teacher.models import ClassRoom , Teacher
from student.models import Student

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
        


class TeacherListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated] 
    
    def get(self,request):
        teacher = User.objects.filter(role__name__icontains='teacher')
        serializer = TeacherListSerializer(teacher, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        teacher_serializer = TeacherPostSerializer(data=request.data)

        if user_serializer.is_valid(raise_exception=True) and (
            teacher_serializer.is_valid(raise_exception=True)
            ):
            user_instance = user_serializer.save()
            teacher_serializer.save(user=user_instance)   
            return Response(
                {"message": "Teacher created successfully"}, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": "Error creating teacher"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
        
        
class TeacherGetUpdateViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = TeacherGetUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    
    def retrieve(self, request, *args, **kwargs):
        try:
            teacher_id = kwargs.get('pk')
            teacher = User.objects.get(id=teacher_id , role__name__icontains='teacher')
            serializer = self.get_serializer(teacher)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error":"Teacher not found"},status=status.HTTP_404_NOT_FOUND)
        
        
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            print(instance)
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response("Teacher deleted successfully",status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Msg":"Teacher not found"},status=status.HTTP_404_NOT_FOUND)
        
    

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
            student_serializer.save(user=user_instance)          
            return Response(
                {"message": "Student created successfully"}, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": "Error creating teacher"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
            
            
class StudentGetUpdateViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = StudentGetUpdateSerializer
    permission_classes = [IsAuthenticated]
    
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
            print(instance)
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response("Teacher deleted successfully",status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Msg":"Teacher not found"},status=status.HTTP_404_NOT_FOUND)
        

      
            
class ClassRoomViewset(viewsets.ModelViewSet):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save()
         