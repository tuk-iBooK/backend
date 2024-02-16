from .models import User, UserProfile
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password", "nickname")

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            nickname=validated_data["nickname"],
            password=validated_data["password"],
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    
    # User model에서 nickname 필드 사용
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    
    class Meta: 
        model = UserProfile
        fields = ["user_nickname", "age", "gender", "description"]