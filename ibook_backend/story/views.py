from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from .models import Background, Character, Story
from .serializers import CharacterSerializer, StorySerializer, BackgroundSerializer

import os
import openai
import requests
import random
import datetime
from io import BytesIO

import boto3
from PIL import Image


@permission_classes([IsAuthenticated])
class StoryAPIView(APIView):
    def post(self, request):

        serializer = StorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response(
                {
                    "message": "Story created successfully.",
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class CharacterAPIView(APIView):
    def post(self, request):

        serializer = CharacterSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "Character created successfully.",
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class BackgroundAPIView(APIView):
    def post(self, request):
        serializer = BackgroundSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "Character created successfully.",
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatgptAPIView(APIView):

    # background, character를 이용하여 이야기 제작 시작
    @permission_classes([AllowAny])
    def post(self, request):
        story_id = request.data.get("story_id", None)

        if story_id is None:
            return Response({"error": "story_id is required"}, status=400)

        story = get_object_or_404(Story, pk=story_id)

        background = Background.objects.filter(story=story).first()
        characters = Character.objects.filter(story=story)

        # OpenAI API 키를 설정 파일에서 가져옴
        openai.api_key = settings.OPENAI_API_KEY

        # 사용할 모델 설정
        model = "gpt-3.5-turbo"

        # ChatGPT API를 사용하여 응답 생성
        # 메시지에 Background 및 Characters 정보를 추가하여 ChatGPT에 전달합니다.
        messages = []

        if background:
            background_info = f"Background: {background.genre}, {background.time_period}, {background.back_ground}, Summary: {background.summary}"
            messages.append({"role": "system", "content": background_info})

        if characters:
            characters_info = "\n".join(
                [
                    f"Character: {char.name}, Age: {char.age}, Gender: {char.gender}, Personality: {char.personality}"
                    for char in characters
                ]
            )
            print(characters_info)
            messages.append({"role": "system", "content": characters_info})

        messages.append(
            {
                "role": "system",
                "content": "주어진 정보를 토대로 어린이들을 위한 동화를 제작해줘.",
            }
        )
        print(messages)
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            # temperature=0.7,  # 창의성을 조절
            # max_tokens=300,  # 생성할 최대 토큰 수
        )

        # 생성된 응답 추출
        answer = response["choices"][0]["message"]["content"]

        # 생성된 응답 반환
        return Response({"answer": answer})
    
class ChatgptImageAPIView(APIView):
    @permission_classes([AllowAny])
    def post(self, request):
        query = request.data.get("query", None)
        
        if query is None:
            return Response({"error": "query is required"}, status=400)
        
        image_url = delleIMG(query)

        return Response({"image_url": image_url})

def delleIMG(query):
    openai.api_key = settings.OPENAI_API_KEY

    model = "gpt-3.5-turbo"

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant who is good at translating.",
        },
        {"role": "assistant", "content": query},
    ]

    # 사용자 메시지 추가
    messages.append({"role": "user", "content": "영어로 번역해주세요."})

    # ChatGPT API 호출하기
    response = openai.ChatCompletion.create(model=model, messages=messages)
    answer3 = response["choices"][0]["message"]["content"]
    # 새 메시지 구성
    messages = [
        {
            "role": "system",
            "content": "You are an assistant who is good at creating prompts for image creation.",
        },
        {"role": "assistant", "content": answer3},
    ]

    # 사용자 메시지 추가
    messages.append(
        {
            "role": "user",
            "content": "Condense up to 4 outward description to focus on nouns and adjectives separated by ,",
        }
    )

    # ChatGPT API 호출하기
    response = openai.ChatCompletion.create(model=model, messages=messages)
    answer4 = response["choices"][0]["message"]["content"]
    print(answer4)

    # 이미지 생성을 위한 프롬프트
    params = ", concept art, realistic lighting, ultra-detailed, 8K, photorealism, digital art"
    prompt = f"{answer4}{params}"
    print(prompt)

    response = openai.Image.create(prompt=prompt, n=1, size="512x512")
    image_url = response["data"][0]["url"]
    print(image_url)
    
    # 이미지 다운로드
    res = requests.get(image_url)
    if res.status_code != 200:
        return Response({"error" : "Failed to download image"}, status=400)
    
    # 이미지 열기
    img = Image.open(BytesIO(res.content))
    
    # S3에 이미지 저장
    # 고유한 키 이름 생성
    now = datetime.datetime.now()
    random_suffix = random.randint(1000, 9999)
    s3_filename = f'images/{now.strftime("%Y-%m-%d-%H-%M-%S")}_{random_suffix}.png'
    
    s3_bucket = settings.AWS_STORAGE_BUCKET_NAME
    print(s3_bucket)
    
    save_image_to_s3(img, s3_bucket, s3_filename)
    
    # 저장된 이미지의 URL 생성
    aws_s3_download_url = os.environ.get('AWS_S3_DOWNLOAD_UAL')
    image_s3_url = f'{aws_s3_download_url}/{s3_filename}'
    print(image_s3_url)
    
    return image_s3_url

def save_image_to_s3(image, bucket_name, file_name):
    try:
        # S3에 이미지 업로드
        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )
        with BytesIO() as output:
            image.save(output, format="PNG")
            output.seek(0)
            s3.upload_fileobj(output, bucket_name, file_name)
        print(
            f"Image saved successfully to S3 bucket: {bucket_name}, with file name: {file_name}"
        )
        return True
    except Exception as e:
        print(f"Failed to save image to S3: {str(e)}")
        return False