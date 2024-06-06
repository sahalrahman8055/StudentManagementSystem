from django.urls import path , include
from teacher.views import TeacherLoginAPIView ,  StudentViewset
# TeacherClassStudentsAPIView , TeacherBusStudentsAPIView , StudentBusServiceAPIView ,
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'stud', StudentViewset )


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
