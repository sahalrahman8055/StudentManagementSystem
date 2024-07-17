from rest_framework.routers import DefaultRouter
from django.urls import path, include
from admins.views import (
    AdminLoginAPIView,
    TeacherViewSet,
     ClassRoomViewset ,
    #  TeacherListCreateAPIView ,
    #  StudentListCreateAPIView ,
    #  TeacherGetUpdateViewset,
    #  StudentGetUpdateViewset,
    ClassTeacherViewset,
    StudentViewSet,
    StudentsUploadViewset
)


router = DefaultRouter()
router.register(r"teachers", TeacherViewSet, basename="teacher")
router.register(r"student", StudentViewSet, basename="student")
router.register(r"classteacher", ClassTeacherViewset, basename="classTeacher")
router.register(r"classroom", ClassRoomViewset, basename="ClassRoom")
router.register(r"upload", StudentsUploadViewset, basename="upload")


urlpatterns = [
    path("login/", AdminLoginAPIView.as_view(), name="login"),
    path("", include(router.urls)),
]
