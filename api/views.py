from django.db.models import QuerySet
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login,get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import permissions, status
from rest_framework.response import Response
from users import serializers as my_serializers
from django.shortcuts import get_object_or_404
from users.models import Client, ServiceProvider, Service, CustomUser

User = get_user_model()


class LoginAPIView(APIView):
    serializer_class = my_serializers.LoginSerializer
    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            Token.objects.get(user=user).delete()
            token = Token.objects.create(user=user).key
            login(request, user)
            return Response({
                "status": status.HTTP_200_OK,
                'data': {
                    'id': user.id,
                    'name': user.name,
                    'username': user.username,
                    'email': user.email,
                    'type': user.type,
                    'token': token
                }
            })
        else:
            return Response({
                "status": status.HTTP_401_UNAUTHORIZED,
                "message": "invalid login credentials",
                "data": "Invalid Username or Password",
            })


class ClientSignUpAPIView(generics.CreateAPIView):
    serializer_class = my_serializers.ClientSignUpSerializer
    permission_classes = [
        permissions.AllowAny,  # Or anon users can't register
    ]

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        new_user = User.objects.get(id=response.data['id'])
        client_obj = Client.objects.create(
            user=new_user,
            address=request.data['address'],
            postal_code=request.data['postal_code'],
            phone=request.data['phone'],
            country=request.data['country'],
        )
        client_obj.save()
        token = Token.objects.get(user=response.data['id']).key
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({
                'status': response.status_code,
                'message': 'User Created',
                'data': {
                    'id': response.data['id'],
                    'username': response.data['username'],
                    'name': response.data['name'],
                    'email': response.data['email'],
                    'type': response.data['type'],
                    'address': client_obj.address,
                    'postal_code': client_obj.postal_code,
                    'phone': client_obj.phone,
                    'country': client_obj.country,
                    'token': token
                }
            })
        else:
            print('invalid login credentials')
            return Response({
                'status': response.status_code,
                'message': 'Invalid Login',
                'data': 'Invalid Username or Password',
            })


class ServiceProviderSignUpAPIView(generics.CreateAPIView):
    serializer_class = my_serializers.ServiceProviderSignUpSerializer
    permission_classes = [
        permissions.AllowAny,  # Or anon users can't register
    ]

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        new_user = User.objects.get(id=response.data['id'])
        sp_obj = ServiceProvider.objects.create(
            user=new_user,
            address=request.data['address'],
            full_name=request.data['full_name'],
            company_name=request.data['company_name'],
            phone=request.data['phone'],
            country=request.data['country'],
            business_phone=request.data['business_phone'],
            licensed=request.data['licensed'],
            postal_code=request.data['postal_code']
        )
        sp_obj.save()
        token = Token.objects.get(user=response.data['id']).key
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({
                'status': response.status_code,
                'message': 'User Created',
                'data': {
                    'id': response.data['id'],
                    'username': response.data['username'],
                    'name': response.data['name'],
                    'email': response.data['email'],
                    'type': response.data['type'],
                    'address': sp_obj.address,
                    'full_name': sp_obj.full_name,
                    'company_name': sp_obj.company_name,
                    'phone': sp_obj.phone,
                    'business_phone': sp_obj.business_phone,
                    'country': sp_obj.country,
                    'licensed': sp_obj.licensed,
                    'token': token
                }
            })
        else:
            print('invalid login credentials')
            return Response({
                'status': response.status_code,
                'message': 'Invalid Login',
                'data': 'Invalid Username or Password',
            })


class ServiceProviderUpdateAPIView(generics.UpdateAPIView):
    serializer_class = my_serializers.ServiceProviderSerializer


class ClientUpdateAPIView(generics.UpdateAPIView):
    serializer_class = my_serializers.ClientSerializer

    def get_object(self):
        queryset = self.get_queryset()
        # obj = get_object_or_404(queryset, user=self.request.user)
        obj = get_object_or_404(queryset)
        return obj

    def get_queryset(self):
        client_id = self.request.data['id']
        return Client.objects.filter(id=client_id)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ServiceCreateAPIView(generics.CreateAPIView):
    serializer_class = my_serializers.ServiceSerializer


class ServiceUpdateAPIView(generics.UpdateAPIView):
    serializer_class = my_serializers.ServiceSerializer


class ServiceListAPIView(generics.ListAPIView):
    serializer_class = my_serializers.ServiceSerializer

    def get_object(self):
        queryset = self.get_queryset()
        # obj = get_object_or_404(queryset, user=self.request.user)
        obj = get_object_or_404(queryset)
        return obj

    def get_queryset(self):

        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset


class UserDataRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = my_serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        queryset = self.get_queryset()
        # obj = get_object_or_404(queryset, user=self.request.user)
        obj = get_object_or_404(queryset)
        return obj

    def get_queryset(self):
        user = self.kwargs.get('user_id', '')
        return CustomUser.objects.filter(id=user)

    def post(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ClientDataRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = my_serializers.ClientSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        queryset = self.get_queryset()
        # obj = get_object_or_404(queryset, user=self.request.user)
        obj = get_object_or_404(queryset)
        return obj

    def get_queryset(self):
        client_id = self.kwargs.get('client_id', '')
        return Client.objects.filter(user=client_id)

    def post(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ServiceProviderDataRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = my_serializers.ServiceProviderSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        queryset = self.get_queryset()
        # obj = get_object_or_404(queryset, user=self.request.user)
        obj = get_object_or_404(queryset)
        return obj

    def get_queryset(self):
        service_provider = self.kwargs.get('sp_id', '')
        return ServiceProvider.objects.filter(user=service_provider)

    def post(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
