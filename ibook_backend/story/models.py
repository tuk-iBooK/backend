from django.db import models

from users.models import User


class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_story")
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ChatLog(models.Model):
    story = models.ForeignKey(
        Story, on_delete=models.CASCADE, related_name="story_chatlog"
    )
    chat_log = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Character(models.Model):
    story = models.ForeignKey(
        Story, on_delete=models.CASCADE, related_name="story_character"
    )
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    name = models.CharField(max_length=20)
    personality = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StoryContent(models.Model):
    story = models.ForeignKey(
        Story, on_delete=models.CASCADE, related_name="story_content"
    )
    page = models.IntegerField()
    content = models.TextField()
    image = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Background(models.Model):
    GENRE_CHOICES = (
        ("fantasy", "Fantasy"),
        ("adventure", "Adventure"),
        ("fairy_tale", "Fairy Tale"),
        ("mythology", "Mythology"),
        ("science_fiction", "Science Fiction"),
    )
    story = models.ForeignKey(
        Story, on_delete=models.CASCADE, related_name="story_background"
    )
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES)
    time_period = models.CharField(max_length=100)
    back_ground = models.CharField(max_length=100)
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
