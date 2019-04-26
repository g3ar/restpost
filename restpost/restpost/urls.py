from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token
)

from restpost.api import UserViewSet, SignupUserView
from post.api import PostViewSet, LikeViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'likes', LikeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url('api/', include(router.urls)),
    url('auth/', include('rest_framework.urls', namespace='rest_framework')),
    url('auth/signup/', SignupUserView.as_view()),
    url('jwt/get/', obtain_jwt_token),
    url('jwt/refresh/', refresh_jwt_token),
    url('jwt/verify/', verify_jwt_token),
]
