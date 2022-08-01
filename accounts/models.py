from django.db import models
from django.db.models.base import Model
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    username = models.CharField(default='', max_length=50)
    email = models.EmailField(('email address'), unique=True)
    phone = models.CharField(('phone address'), max_length=10)
    bio = models.TextField(default="Hello World")
    country = CountryField()
    avatar = models.ImageField(default="avatar.png", upload_to="avatars")
    report = models.ManyToManyField('self', blank=True)
    slug = models.SlugField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class SocialProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    slack = models.URLField(blank=True, null=True)
    
