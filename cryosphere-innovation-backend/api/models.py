import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import ImageField


class Instrument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True)
    serial_number = models.CharField(max_length=100, null=True)
    notes = models.TextField(max_length=5000, null=True, blank=True)
    description = models.TextField(max_length=2000, null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)
    starred = models.BooleanField(default=False)
    starred_date = models.DateTimeField(null=True, blank=True)
    purchase_date = models.DateTimeField(null=True, blank=True)
    template = models.BooleanField(default=False)
    data_model = models.JSONField(null=True)
    active_deployment = models.JSONField(null=True)
    general = models.JSONField(null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name


class DeploymentTags(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7)

    def __str__(self):
        return self.name


class Deployment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=20, null=True)
    collaborators = models.ManyToManyField(
        User, related_name='collaborators', blank=True)
    instrument = models.ForeignKey(
        Instrument, on_delete=models.CASCADE, null=True)
    location = models.CharField(max_length=500, null=True)
    description = models.TextField(max_length=2000, null=True, blank=True)
    notes = models.TextField(max_length=5000, null=True, blank=True)
    deployment_start_date = models.DateTimeField(null=True)
    deployment_end_date = models.DateTimeField(null=True)
    private = models.BooleanField(default=True, null=True)
    tags = models.ManyToManyField(DeploymentTags, blank=True)
    starred = models.BooleanField(default=False, null=True)
    starred_date = models.DateTimeField(null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name
