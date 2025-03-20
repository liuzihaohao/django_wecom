from django.contrib.auth.models import AbstractUser, Group
from django.db import models

from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        email = self.normalize_email(email)
        if self.model.objects.last():
            extra_fields.setdefault("id", self.model.objects.last().id+1)
        else:
            extra_fields.setdefault("id", 1)
        extra_fields.setdefault("is_active", True)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    """
    自定义用户表
    """
    id = models.CharField(primary_key=True, unique=True, max_length=200) # 企微是字符串 ID
    real_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="真实姓名")

    objects = UserManager()

    def __str__(self):
        return (self.real_name if self.real_name else "None") + " - " + self.username

class Group(Group):
    class Meta:
        proxy = True
        verbose_name = "组"
        verbose_name_plural = "组"