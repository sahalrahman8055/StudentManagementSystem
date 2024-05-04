from django.urls import path , include
from admins.views import AdminLoginAPIView, AdminTeacherRegisterViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'teacher', AdminTeacherRegisterViewset)


urlpatterns = [
    path('login/',AdminLoginAPIView.as_view(),name='login'),
    
    path('', include(router.urls)),
]
