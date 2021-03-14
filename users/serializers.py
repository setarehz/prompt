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


class ClientSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = [
            'id', 'username', 'password', 'email', 'name', 'type'
        ]
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        new_user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data['name'],
            type=validated_data['type']
        )
        new_user.set_password(validated_data['password'])
        new_user.save()

        return new_user


class ServiceProviderSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ('id', 'username', 'password', 'email', 'name', 'type')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        new_user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data['name'],
            type=validated_data['type']
        )
        new_user.set_password(validated_data['password'])
        new_user.save()

        return new_user


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = my_models.Service


class ServiceProviderSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = my_models.ServiceProvider
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = my_models.Client
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = my_models.CustomUser
        fields = '__all__'
