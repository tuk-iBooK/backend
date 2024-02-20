from django.contrib import admin
from django.urls import path
from users.views import AuthAPIView, RegisterAPIView, UserProfileView
from story.views import CharacterAPIView, StoryAPIView, BackgroundAPIView, UserStoryAPIView
from story.views import ChatgptAPIView, ChatgptImageAPIView, StoryContentAPIView

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/register/", RegisterAPIView.as_view()),
    path("api/auth/login/", AuthAPIView.as_view()),
    path("api/auth/me/", AuthAPIView.as_view()),
    path("api/user/profile/", UserProfileView.as_view()),
    path("api/user/story/", UserStoryAPIView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),
    path("api/story/register/character/", CharacterAPIView.as_view()),
    path("api/story/register/", StoryAPIView.as_view()),
    path("api/story/", StoryAPIView.as_view()),
    path("api/story/register/background/", BackgroundAPIView.as_view()),
    path("api/story/register/chatgpt/", ChatgptAPIView.as_view()),
    path("api/story/register/chatgpt/image/", ChatgptImageAPIView.as_view()),
    path("api/story-content/", StoryContentAPIView.as_view()),
]
