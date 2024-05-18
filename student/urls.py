from django.urls import path , include
from student.views import (
    AssignBusServiceAPIView
)


urlpatterns = [
     path('schoolbus/<int:student_id>/', AssignBusServiceAPIView.as_view(), name='student-bus-update'),
]
