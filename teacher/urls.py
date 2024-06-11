from django.urls import path, include
from teacher.views import TeacherLoginAPIView, StudentViewset, BusStudentsViewset , PaymentViewset

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"students", StudentViewset, basename="class_Students")
router.register(r"busStudent", BusStudentsViewset, basename="busservice_student")
router.register(r"payment", PaymentViewset, basename="payment")



urlpatterns = [
    path("login/", TeacherLoginAPIView.as_view(), name="teacher-login"),
    path('payment/get_user_payments/<int:user_id>/', PaymentViewset.as_view({'get': 'get_user_payments'}), name='get-user-payments'),
    path("", include(router.urls)),
]
