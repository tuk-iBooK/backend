from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, nickname, password):
        if not email:
            raise ValueError("이메일을 작성해주세요")

        if self.model.objects.filter(nickname=nickname).exists():
            raise ValueError("이미 사용중인 닉네임입니다.")

        if not password:
            raise ValueError("비밀번호를 입력해주세요")

        user = self.model(email=self.normalize_email(email), nickname=nickname)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password):
        if not password:
            raise ValueError("비밀번호를 입력해주세요")

        user = self.create_user(
            email=self.normalize_email(email), nickname=nickname, password=password
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    email = models.EmailField(max_length=255, unique=True)
    nickname = models.CharField(max_length=10, unique=True)  # 닉네임에 대한 고유성 보장
    created_on = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class UserProfile(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_profile"
    )
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)