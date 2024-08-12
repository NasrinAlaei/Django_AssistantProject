from django.db import models
from django.contrib.auth.models import AbstractUser
import base64
# Create your models here.

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='pics', blank=True, default='pics/avatar.jpg')         
    
    # data = models.CharField(max_length=100)
