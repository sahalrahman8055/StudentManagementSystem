from rest_framework.views import APIView
from student.models import Student
from schoolbus.models import Bus,BusPoint,Route
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    StudentBusSerializer,
    StudentBusGetSerializer,
    StudentSerializer,
    StudentBusssSerializer,
    BusAssignmentSerializer
)
from django.db import transaction
from django.db.models import Q


# class StudentBusAPIView(APIView):
    
#     def put(self,request,student_id):

#         student = Student.objects.get(user_id=student_id)
        
#         bus_id = request.data.get('bus')
#         route_id = request.data.get('route')
#         bus_point_id = request.data.get('bus_point')
#         print(bus_id)
#         print(route_id)
#         print(bus_point_id)
        
#         if bus_id:
#             try:
#                 bus = Bus.objects.get(id=bus_id)
#                 print(bus,'55555555')
#                 student.bus = bus
#             except Bus.DoesNotExist:
#                 return Response({'error': 'Bus not found'}, status=status.HTTP_404_NOT_FOUND)
#         else:
#             return Response({'error': 'Bus_id not found'}, status=status.HTTP_400_BAD_REQUEST)

#         # Validate and update route
#         if bus and route_id:
#             route = bus.routes.filter(id=route_id).first()
#             if not route:
#                 return Response(
#                     {"msg": "Route does not belong to the specified bus"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#             student.route = route
#         else:
#             return Response({'error': 'route_id not found'}, status=status.HTTP_400_BAD_REQUEST)

#         # Validate and update bus point
#         if route and bus_point_id:
#             bus_point = route.bus_points.filter(id=bus_point_id).first()
#             if not bus_point:
#                 return Response(
#                     {"msg": "BusPoint does not belong to the specified route"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#             student.bus_point = bus_point
#         else:
#             return Response({'error': 'bus_point_id not found'}, status=status.HTTP_400_BAD_REQUEST)

#         student.save()
        
#         serializer = StudentBusSerializer(student)
#         return Response(
#             {'message': 'Student bus service updated successfully', 'data': serializer.data},
#             status=status.HTTP_200_OK
#         )

# class StudentBusAPIView(APIView):
#       # def get(self, request):
#       def get(self, request,student_id):
#           students_with_bus_details = Student.objects.select_related('bus').all()
#           serializer = StudentBusGetSerializer(students_with_bus_details, many=True)
#           return Response(serializer.data)
          
            
#       @transaction.atomic
#       def put(self, request, student_id):

          
#           student = Student.objects.get(user_id=student_id)

#           # Extract data from the request
#           bus_id = request.data.get('bus_id')
#           route_id = request.data.get('route_id')
#           bus_point_id = request.data.get('bus_point_id')
#           # Initialize bus and route variables
#           bus = None
#           route = None

#           # Validate and update bus
#           if bus_id:
#               try:
#                   bus = Bus.objects.get(id=bus_id)
#                   student.bus = bus
#               except Bus.DoesNotExist:
#                   return Response({'error': 'Bus not found'}, status=status.HTTP_404_NOT_FOUND)

#           # Validate and update route
#           if bus and route_id:
#               route = bus.routes.filter(id=route_id).first()
#               if not route:
#                   return Response(
#                       {"msg": "Route does not belong to the specified bus"},
#                       status=status.HTTP_400_BAD_REQUEST
#                   )
#               student.route = route

#           # Validate and update bus point
#           if route and bus_point_id:
#               bus_point = route.bus_points.filter(id=bus_point_id).first()
#               if not bus_point:
#                   return Response(
#                       {"msg": "BusPoint does not belong to the specified route"},
#                       status=status.HTTP_400_BAD_REQUEST
#                   )
#               student.bus_point = bus_point

#           # Save the student instance
#           student.save()

#           # Serialize and return the updated student
#           serializer = StudentBusSerializer(student)
#           return Response(
#               {'message': 'Student bus service updated successfully', 'data': serializer.data},
#               status=status.HTTP_200_OK
#           )




class AssignBusServiceAPIView(APIView):
  
    def get(self, request, student_id):
        try:
            student = Student.objects.select_related('bus', 'route', 'bus_point').get(user_id=student_id)
        except Student.DoesNotExist:
            return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)
  
  
    def put(self, request, student_id):
        serializer = BusAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            route_number = serializer.validated_data['route_number']
            bus_point_id = serializer.validated_data['bus_point_id']
            
            try:
                route = Route.objects.get(route_no=route_number, bus_points__id=bus_point_id)
                bus_point = BusPoint.objects.get(id=bus_point_id)
            except Route.DoesNotExist:
                return Response({"error": "No matching route found."}, status=status.HTTP_404_NOT_FOUND)
            except BusPoint.DoesNotExist:
                return Response({"error": "No matching bus point found."}, status=status.HTTP_404_NOT_FOUND)

            bus_service = route.bus
            print(bus_service, '5555555')
            
            try:
                student = Student.objects.get(user_id=student_id)
            except Student.DoesNotExist:
                return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

            student.bus = bus_service
            student.route = route
            student.bus_point = bus_point
            student.save()
            serializer = StudentBusssSerializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)