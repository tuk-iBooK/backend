from django.contrib import admin
from django.urls import path
from users.views import AuthAPIView, RegisterAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/register/", RegisterAPIView.as_view()),
    path("api/auth/login/", AuthAPIView.as_view()),
    path("api/auth/me/", AuthAPIView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),
]
