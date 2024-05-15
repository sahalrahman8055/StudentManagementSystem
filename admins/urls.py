from rest_framework.routers import DefaultRouter
from django.urls import path , include
from admins.views import (
     AdminLoginAPIView , 
     ClassRoomViewset , 
     TeacherListCreateAPIView , 
     StudentListCreateAPIView ,
     TeacherGetUpdateViewset,
     StudentGetUpdateViewset
)

router = DefaultRouter()
# router.register(r'teacher', AdminTeacherRegisterViewset)
router.register(r'classroom', ClassRoomViewset)
router.register(r'teacher', TeacherGetUpdateViewset,basename='teacher')
router.register(r'student', StudentGetUpdateViewset,basename='student')


urlpatterns = [
    path(
        'login/',
        AdminLoginAPIView.as_view(),
        name='login'
    ),
    path('', include(router.urls)),
    path(
        'register/teacher/',
         TeacherListCreateAPIView.as_view(),
         name='teacher'
    ),
    path(
        'register/student/', 
        StudentListCreateAPIView.as_view(),
        name='student'
    ),
]
