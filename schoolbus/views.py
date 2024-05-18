from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView 
from rest_framework.permissions import IsAuthenticated
from schoolbus.serializers import (
    BusSerializer,
    RouteSerializer,
    BusRouteSerializer
) 
from schoolbus.models import Bus , Route , BusPoint




class BusViewset(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    
    def perform_create(self, serializer):
        serializer.save()
        
        

        
class RouteViewset(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
              {'message': 'Route created successfully', 
              'data': serializer.data}, 
                status=status.HTTP_201_CREATED, headers=headers
        )
        
        

class BusPointViewset(viewsets.ModelViewSet):
    queryset = BusPoint.objects.all()
    serializer_class = BusRouteSerializer