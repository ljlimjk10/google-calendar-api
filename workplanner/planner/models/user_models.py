from django.db import models    
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from . import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=300, unique=True)
    email = models.CharField(max_length=400, unique=True)
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email