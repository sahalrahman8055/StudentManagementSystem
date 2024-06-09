from django.urls import path, include
from student.views import (
    AssignBusServiceAPIView,
    BusPointSearchAPIView,
    StudentsByRouteAPIView,
)


urlpatterns = [
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
