from django.urls import path, include
from teacher.views import StudentViewset, BusStudentsViewset , PaymentCreateAPIView , TransactionViewset , TeacherProfileViewset

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"profile", TeacherProfileViewset, basename="teacher-profile")
router.register(r"students", StudentViewset, basename="class_Students")
router.register(r"busStudent", BusStudentsViewset, basename="busservice_student")
router.register(r"transactions", TransactionViewset, basename="transactions-get-transactions")



urlpatterns = [
    path('payment/', PaymentCreateAPIView.as_view(), name='payment-list-create'),
    path("", include(router.urls)),
]
