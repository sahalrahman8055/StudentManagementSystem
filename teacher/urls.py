from django.urls import path, include
from teacher.views import TeacherLoginAPIView, StudentViewset, BusStudentsViewset , PaymentCreateAPIView , TransactionViewset

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"students", StudentViewset, basename="class_Students")
router.register(r"busStudent", BusStudentsViewset, basename="busservice_student")
router.register(r"transactions", TransactionViewset, basename="transactions-get-transactions")



urlpatterns = [
    path("login/", TeacherLoginAPIView.as_view(), name="teacher-login"),
    path('payment/', PaymentCreateAPIView.as_view(), name='payment-list-create'),
    path("", include(router.urls)),
]
