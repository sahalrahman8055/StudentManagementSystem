from django.urls import path, include
from rest_framework.routers import DefaultRouter
from schoolbus.views import (
    BusViewset,
    RouteViewset,
    BusPointViewset,
)

router = DefaultRouter()
router.register(r"bus", BusViewset, basename="bus")
router.register(r"routes", RouteViewset, basename="route")
router.register(r"buspoint", BusPointViewset, basename="buspoint")


urlpatterns = [
    path("", include(router.urls)),
]
