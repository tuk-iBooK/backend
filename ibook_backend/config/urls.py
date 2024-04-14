from django.contrib import admin
from django.urls import path
from users.views import AuthAPIView, RegisterAPIView, UserProfileView
from story.views import (
    CharacterAPIView,
    StoryAPIView,
    BackgroundAPIView,
    UserStoryAPIView,
)
from story.views import (
    ChatgptAPIView,
    ChatgptImageAPIView,
    StoryContentAPIView,
    SaveStoryAPIView,
)

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    # 회원 관련 API
    path("api/auth/register/", RegisterAPIView.as_view()),
    path("api/auth/login/", AuthAPIView.as_view()),
    path("api/auth/me/", AuthAPIView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),
    
    # 유저 프로필 & 만든 이야기 API
    path("api/user/profile/", UserProfileView.as_view()),
    path("api/user/story/", UserStoryAPIView.as_view()),
    
    # 이야기, 이야기 내용 조회 및 이야기 초기 설정 API
    path("api/story/", StoryAPIView.as_view()),
    path("api/story-content/", StoryContentAPIView.as_view()),
    path("api/story/register/character/", CharacterAPIView.as_view()),
    path("api/story/register/", StoryAPIView.as_view()),
    path("api/story/register/background/", BackgroundAPIView.as_view()),
    
    # 이야기 생성 & 저장 및 그림 생성 & 저장 API
    path("api/story/register/chatgpt/", ChatgptAPIView.as_view()),
    path("api/story/register/chatgpt/image/", ChatgptImageAPIView.as_view()),
    path("api/story/save_story/", SaveStoryAPIView.as_view()),
]