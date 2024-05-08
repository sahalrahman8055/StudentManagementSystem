from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from teacher.serializers import TeacherLoginSerializer
from rest_framework.views import APIView 
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from admins.utilities.token import get_tokens_for_user
from admins.models import User , Role
from rest_framework.permissions import IsAuthenticated
import logging

logger = logging.getLogger(__name__)


class TeacherLoginAPIView(APIView):
    def post(self, request):
      serializer = TeacherLoginSerializer(data=request.data)
      try:
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
              login(request, user)
              token = get_tokens_for_user(user)
              return Response(
                  {'message': 'Login successful', 'token':token}, 
                  status=status.HTTP_200_OK
              )
            logger.warning("User authentication failed: No user found with provided credentials.")
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      except Exception as e:
            logger.exception("An error occurred during user authentication:")
            return Response({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)