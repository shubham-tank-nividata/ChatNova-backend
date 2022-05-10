from email.policy import default
from operator import mod
from django.db import models
from django.contrib.auth.models import User
import datetime
from core import settings

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    image = models.ImageField(default='default_profile.jpg',upload_to='profile_pics')
    bio = models.CharField(max_length=500,blank=True, null=True)