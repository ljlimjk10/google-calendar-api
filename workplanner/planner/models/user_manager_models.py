from django.db import models
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    
    def create_user(self,username,email,password=None):
        if not username:
            raise ValueError('User must have an username')
        if not email:
            raise ValueError('User must have an email')
        
        email = self.normalize_email(email)
        user = self.model(username=username,email=email)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self,username,email,password):
        user = self.create_user(username=username,email=email,password=password)
        user.is_superuser=True
        user.is_staff = True
        user.save(using=self.db)
        return user

