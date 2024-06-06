from django.urls import path , include
from teacher.views import TeacherLoginAPIView ,  StudentViewset , BusStudentsViewset
# TeacherClassStudentsAPIView , TeacherBusStudentsAPIView , StudentBusServiceAPIView ,
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'students', StudentViewset, basename="classStudents" )
router.register(r'busStudent', BusStudentsViewset, basename="yoy" )


urlpatterns = [
    path('login/',
         TeacherLoginAPIView.as_view(),
         name='teacher-login'
    ),
#     path('classstudents/',
#          TeacherClassStudentsAPIView.as_view(),
#          name='class-students'
#     ),
#     path('busstudents/',
#          TeacherBusStudentsAPIView.as_view(),
#          name='class-bus-students'
#     ),
#     path('busService/<int:student_id>/',
#          StudentBusServiceAPIView.as_view(),
#          name='class-bus-students'
#     ),
    path('',include(router.urls))
    
]
