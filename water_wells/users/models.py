# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    # Diğer özel alanlarınızı burada tanımlayın
    objects = CustomUserManager()

    is_premium = models.BooleanField(default=False)
    # Diğer özel alanlarınızı burada tanımlayın
