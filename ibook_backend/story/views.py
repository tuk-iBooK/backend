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

import openai


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