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
router.register("teachers", TeacherViewSet, basename="teacher")
router.register("student", StudentViewSet, basename="student")
router.register("classteacher", ClassTeacherViewset, basename="classTeacher")
router.register("classroom", ClassRoomViewset, basename="ClassRoom")
router.register("upload", StudentsUploadViewset, basename="upload")


urlpatterns = [
    path("login/", AdminLoginAPIView.as_view(), name="login"),
    path("", include(router.urls)),
]
