from rest_framework.views import APIView
from student.models import Student, StudentBusService , ClassRoom
from schoolbus.models import Bus, BusPoint, Route
from rest_framework.response import Response
from rest_framework import status
from student.serializers import (
    StudentBusServiceSerializer,
    StudentBusSerializer,
    BusAssignmentSerializer,
    RouteListSerializer,
    StudentByRouteSerializer,
    StudentDetailSerializer
)
from rest_framework import viewsets
from rest_framework.decorators import action
from admins.utilities.permission import IsAdminUser


class BusPointSearchAPIView(APIView):

    def get(self, request):
        search_query = request.query_params.get("query", None)
        if search_query:
            bus_points = BusPoint.objects.filter(
                name__icontains=search_query
            ).select_related("route", "route__bus")
            if bus_points.exists():
                routes = {bp.route for bp in bus_points}
                serializer = RouteListSerializer(
                    routes, many=True, context={"request": request}
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                {"error": "No routes found for the given bus point name."},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            return Response(
                {"error": "Query parameter 'query' is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class AssignBusServiceAPIView(APIView):

    def get(self, request, student_id):
        try:
            print(f"Received student_id: {student_id}")
            bus_service = StudentBusService.objects.select_related("student").get(
                student__user_id=student_id
            )
            print(f"Found bus service: {bus_service}")
        except StudentBusService.DoesNotExist:
            print("Bus service for student not found.")
            return Response(
                {"error": "Bus service for student not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = StudentBusServiceSerializer(bus_service)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, student_id): 
        serializer = BusAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            route_number = serializer.validated_data["route_number"]
            bus_point_id = serializer.validated_data["bus_point_id"]

            try:
                route = Route.objects.get(
                    route_no=route_number, bus_points__id=bus_point_id
                )
                bus_point = BusPoint.objects.get(id=bus_point_id)
            except Route.DoesNotExist:
                return Response(
                    {"error": "No matching route found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            except BusPoint.DoesNotExist:
                return Response(
                    {"error": "No matching bus point found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            try:
                student = Student.objects.get(user_id=student_id)
            except Student.DoesNotExist:
                return Response(
                    {"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND
                )

            bus_service, created = StudentBusService.objects.get_or_create(
                student=student
            )
            bus_service.bus = route.bus
            bus_service.route = route
            bus_service.bus_point = bus_point
            bus_service.annual_fees = float(bus_point.fee) * 10

            bus = route.bus
            if bus.capacity <= 0:
                return Response(
                    {"error": "No available capacity on this bus."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            bus.capacity = max(bus.capacity - 1, 0)
            bus.save()

            student.is_bus = True
            student.save()

            bus_service.save()

            serializer = StudentBusSerializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentsByRouteAPIView(APIView):

    def get(self, request, route_id):
        try:
            route = (
                Route.objects.select_related("bus")
                .prefetch_related("bus_points")
                .get(id=route_id)
            )
        except Route.DoesNotExist:
            return Response(
                {"error": "Route not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = StudentByRouteSerializer(route)
        return Response(serializer.data, status=status.HTTP_200_OK)




class StudentDetailsViewsets(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('user', 'route__bus', 'classRoom').prefetch_related('route__bus_points')
    serializer_class = StudentDetailSerializer