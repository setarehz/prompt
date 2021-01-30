from rest_framework import serializers
from django.contrib.auth import get_user_model
from users import models as my_models

User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ('id', 'username', 'password', 'email', 'name', 'type')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data['name'],
            type= validated_data['type']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = my_models.ServiceProvider


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = my_models.Service


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = my_models.Client
