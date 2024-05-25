from django.urls import path
from teacher.views import TeacherLoginAPIView , TeacherClassStudentsAPIView , TeacherBusStudentsAPIView , StudentBusServiceAPIView

urlpatterns = [
    path('login/',
         TeacherLoginAPIView.as_view(),
         name='teacher-login'
    ),
    path('classstudents/',
         TeacherClassStudentsAPIView.as_view(),
         name='class-students'
    ),
    path('busstudents/',
         TeacherBusStudentsAPIView.as_view(),
         name='class-bus-students'
    ),
    path('busService/<int:student_id>/',
         StudentBusServiceAPIView.as_view(),
         name='class-bus-students'
    ),
    
]
