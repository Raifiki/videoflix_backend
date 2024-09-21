from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from userAuthentication.views import LoginView, ResetPasswordConfirmView, ResetPasswordView, UserViewSet, VerifyEmailView


router = routers.DefaultRouter()
router.register(r'videoflix/v1/user', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('videoflix/v1/user/verify/<int:user_id>/<str:token>/', VerifyEmailView.as_view()),
    path('videoflix/v1/user/login/', LoginView.as_view()),
    path('videoflix/v1/user/resetpassword/', ResetPasswordView.as_view()),
    path('videoflix/v1/user/resetpasswordconfirm/<int:user_id>/<str:token>/', ResetPasswordConfirmView.as_view()),
    path('',include(router.urls))
]
