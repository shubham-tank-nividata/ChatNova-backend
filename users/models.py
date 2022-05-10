import datetime
from core import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):

    def create_user(self, email, username, password, **other_fields):

        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have a username')

        email = self.normalize_email(email)
        user = self.model(email=email, username = username, **other_fields)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_admin', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True')


        return self.create_user(email, username, password, **other_fields)



class Account(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(verbose_name='email address',unique=True)
    username = models.CharField(max_length=150,unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined',auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = CustomAccountManager()
    
    def __str__(self):
        return self.username
    


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    image = models.ImageField(default='default_profile.jpg',upload_to='profile_pics')
    bio = models.CharField(max_length=500,blank=True, null=True)

    def __str__(self):
        return self.name