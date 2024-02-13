from story.models import Character, Story, Background, StoryContent
from rest_framework import serializers


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ["title"]


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ["story", "age", "gender", "name", "personality"]


class BackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Background
        fields = ["story", "genre", "time_period", "back_ground", "summary"]


class StoryContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryContent
        fields = "__all__"
