from django.urls import path
from teacher.views import TeacherLoginAPIView

urlpatterns = [
    path('login/',TeacherLoginAPIView.as_view())
]
