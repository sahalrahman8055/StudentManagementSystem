from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import AdminLoginSerializer , TeacherRegisterSerializer
from rest_framework.views import APIView 
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from admins.utilities.token import get_tokens_for_user
from admins.models import User , Role
from rest_framework.permissions import IsAuthenticated



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
        



class AdminTeacherRegisterViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = TeacherRegisterSerializer
    permission_classes = [IsAuthenticated]
    
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            print(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    