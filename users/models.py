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


class CustomUser(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    name = models.TextField(verbose_name="Full Name", max_length=128)

    TYPE = (
        ('1', 'Client'),
        ('2', 'ServiceProvider')
    )
    type = models.CharField(max_length=1, choices=TYPE, blank = False, default='1', help_text='usertype')


class ServiceProvider(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='sp_model')
    company_name = models.TextField(max_length=128, null=True)
    full_name = models.TextField(max_length=128, null=True)
    address = models.TextField(max_length=128, null=True)
    postal_code = models.TextField(max_length=128, null=True)
    country = models.TextField(max_length=128, null=True)
    phone = models.TextField(max_length=128, null=True)
    business_phone = models.TextField(max_length=128, null=True)
    licensed = models.BooleanField(default=False)
    coordinate_x = models.TextField(max_length=128)
    coordinate_y = models.TextField(max_length=128)


class Service(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    name = models.TextField(max_length=256)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='services')


class SubService(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    name = models.TextField(max_length=256)
    datetime = models.DateTimeField(auto_now_add=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='sub_services')


class Client(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='client_model')
    address = models.TextField(max_length=128, null=True)
    postal_code = models.TextField(max_length=128, null=True)
    phone = models.TextField(max_length=128, null=True)
    country = models.TextField(max_length=128, null=True)
    services = models.ManyToManyField(Service, related_name='clients', blank=True)
    sub_services = models.ManyToManyField(SubService, related_name='clients', blank=True)
    service_providers = models.ManyToManyField(ServiceProvider, related_name='clients')


class ServiceRequest(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='requests')
    sub_service = models.ForeignKey(SubService, on_delete=models.CASCADE, related_name='requests')
    is_accepted = models.BooleanField(default=False)
