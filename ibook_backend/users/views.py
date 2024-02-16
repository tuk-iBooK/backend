from django.contrib.auth import authenticate
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from .serializers import *
from .models import User, UserProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from rest_framework.response import Response


class RegisterAPIView(APIView):

    @permission_classes([AllowAny])
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "register successs",
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthAPIView(APIView):

    @permission_classes([AllowAny])
    def post(self, request):

        user = authenticate(
            email=request.data.get("email"), password=request.data.get("password")
        )

        if user is not None:
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            return Response(
                {
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "login fail"}, status=status.HTTP_401_UNAUTHORIZED
            )

    @permission_classes([IsAuthenticated])
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)

        return Response(serializer.data)

class UserProfileView(APIView):
    
    @permission_classes([IsAuthenticated])
    def post(self, request):
        
        serializer = UserProfileSerializer(data=request.data)
        
        if serializer.is_valid():
            
            # 유저 정보를 저장할 때 현재 요청을 보낸 유저 정보를 저장
            serializer.save(user=request.user)
            
            return Response(
                {
                    "message": "User Profile created successfully.",
                },
                status=status.HTTP_201_CREATED,
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @permission_classes([IsAuthenticated])
    def get(self, request):
        user = request.user
        
        if not user: 
            Response(
                {"error": "존재하지 않는 유저입니다."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        user_profile = UserProfile.objects.get(user=user)
        
        serializer = UserProfileSerializer(user_profile)
        
        return Response(serializer.data)
    
    @permission_classes([IsAuthenticated])
    def put(self, request):
        user = request.user
        
        if not user: 
            Response(
                {"error": "존재하지 않는 유저입니다."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        user_profile = UserProfile.objects.get(user=user)
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User Profile updated successfully."},
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @permission_classes([IsAuthenticated])
    def delete(self, request):
        user = request.user
        
        if not user:
            return Response(
                {"error": "존재하지 않는 유저입니다."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        user_profile = UserProfile.objects.get(user=user)
        user_profile.delete()
        
        return Response({"message": "User Profile deleted successfully."}, status=status.HTTP_204_NO_CONTENT)