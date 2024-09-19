from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from userAuthentication.views import UserViewSet


router = routers.DefaultRouter()
router.register(r'videoflix/v1/user', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls))
]
