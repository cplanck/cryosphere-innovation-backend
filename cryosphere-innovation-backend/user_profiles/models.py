from django.contrib.auth.models import User
from django.db import models
from django.db.models import ImageField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)
    social_login = models.BooleanField(null=True, blank=True)
    has_social_avatar = models.BooleanField(null=True, blank=True)
    has_made_deployment = models.BooleanField(null=True, blank=True)
    has_made_instrument = models.BooleanField(null=True, blank=True)
