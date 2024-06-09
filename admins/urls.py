from rest_framework.routers import DefaultRouter
from django.urls import path, include
from admins.views import (
    AdminLoginAPIView,
    TeacherViewSet,
    #  ClassRoomViewset ,
    #  TeacherListCreateAPIView ,
    #  StudentListCreateAPIView ,
    #  TeacherGetUpdateViewset,
    #  StudentGetUpdateViewset,
    ClassTeacherViewset,
    StudentViewSet,
)

router = DefaultRouter()
router.register(r"teachers", TeacherViewSet, basename="teacher")
# router.register(r'classroom', ClassRoomViewset)
# router.register(r'teacher', TeacherGetUpdateViewset,basename='teacher')
router.register(r"student", StudentViewSet, basename="student")
router.register(r"classteacher", ClassTeacherViewset, basename="classTeacher")


urlpatterns = [
    path("login/", AdminLoginAPIView.as_view(), name="login"),
    path("", include(router.urls)),
    # path(
    #     'register/teacher/',
    #      TeacherListCreateAPIView.as_view(),
    #      name='teacher'
    # ),
    # path(
    #     'register/student/',
    #     StudentListCreateAPIView.as_view(),
    #     name='students'
    # ),
]
