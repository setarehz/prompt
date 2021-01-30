from enum import auto

from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import uuid


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        if instance.type == 1:
            Client.objects.create(user=instance)
        else:
            if instance.type == 2:
                ServiceProvider.objects.create(user=instance)


class CustomUser(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    name = models.TextField(verbose_name="Full Name", max_length=128)

    class Type(models.IntegerChoices):
        CLIENT = 1
        SERVICE_PROVIDER = 2

    type = models.IntegerField(choices=Type.choices)


class ServiceProvider(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='sp_model')
    name = models.TextField(max_length=128)
    coordinate_x = models.TextField(max_length=128)
    coordinate_y = models.TextField(max_length=128)


class Service(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    name = models.TextField(max_length=256)
    datetime = models.DateTimeField(auto_now_add=True)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='services')


class Client(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='client_model')
    services = models.ManyToManyField(Service, related_name='clients', blank=True, null=True)
    service_providers = models.ManyToManyField(ServiceProvider, on_delete=models.CASCADE, related_name='clients')

