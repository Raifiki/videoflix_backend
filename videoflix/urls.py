from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from userAuthentication.views import LoginView, ResetPasswordConfirmView, ResetPasswordView, UserView, VerifyEmailView
from videoflix import settings
from django.conf.urls.static import static


router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('videoflix/v1/user/', UserView.as_view()),
    path('videoflix/v1/user/verify/', VerifyEmailView.as_view()),
    path('videoflix/v1/user/login/', LoginView.as_view()),
    path('videoflix/v1/user/resetpassword/', ResetPasswordView.as_view()),
    path('videoflix/v1/user/resetpasswordconfirm/', ResetPasswordConfirmView.as_view()),
    path('',include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
