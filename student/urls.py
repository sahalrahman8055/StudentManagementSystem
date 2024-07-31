from django.urls import path, include
from rest_framework.routers import DefaultRouter
from student.views import (
    AssignBusServiceAPIView,
    BusPointSearchAPIView,
    StudentsByRouteAPIView,
    StudentDetailsViewsets
)
router = DefaultRouter()
router.register(r"studentDetail", StudentDetailsViewsets, basename="student-detail")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "schoolbus/<int:student_id>/",
        AssignBusServiceAPIView.as_view(),
        name="student-bus-update",
    ),
    path("buspoints/search/", BusPointSearchAPIView.as_view(), name="buspoint-search"),
    path(
        "route/<int:route_id>/",
        StudentsByRouteAPIView.as_view(),
        name="students-by-route",
    ),
]
