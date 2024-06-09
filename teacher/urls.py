from django.urls import path, include
from teacher.views import TeacherLoginAPIView, StudentViewset, BusStudentsViewset , PaymentViewset

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"students", StudentViewset, basename="class_Students")
router.register(r"busStudent", BusStudentsViewset, basename="busservice_student")
router.register(r"payment", PaymentViewset, basename="payment")


urlpatterns = [
    path("login/", TeacherLoginAPIView.as_view(), name="teacher-login"),
    path('payment/transactions/<int:student_id>/', PaymentViewset.as_view({'get': 'transactions'}), name='student_transactions'),
    path("", include(router.urls)),
]
