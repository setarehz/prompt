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
from users.models import Client, ServiceProvider, Service, CustomUser, SubService

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
                    'sp_uuid': sp_obj.id,
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
    permission_classes = [
        permissions.AllowAny,  # Or anon users can't register
    ]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


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

class ServiceDataRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = my_serializers.ServiceDataRetrieveSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        queryset = self.get_queryset()
        # obj = get_object_or_404(queryset, user=self.request.user)
        obj = get_object_or_404(queryset)
        return obj

    def get_queryset(self):
        service = self.kwargs.get('service_id', '')
        return Service.objects.filter(id=service)

    def post(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ServiceRequestCreateAPIView(generics.CreateAPIView):
    serializer_class = my_serializers.ServiceRequestSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class ServiceAcceptAPIView(generics.UpdateAPIView):
    serializer_class = my_serializers.ServiceAcceptSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def get_queryset(self):
        """
        Get the list of items for this view.
        This must be an iterable, and may be a queryset.
        Defaults to using `self.queryset`.

        This method should always be used rather than accessing `self.queryset`
        directly, as `self.queryset` gets evaluated only once, and those results
        are cached for all subsequent requests.

        You may want to override this if you need to provide different
        querysets depending on the incoming request.

        (Eg. return a list of items that is specific to the user)
        """
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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if request.data['is_accepted']:
            sub_service = instance.sub_service
            client = instance.user
            client.sub_services.add(sub_service)
            client.services.add(sub_service.service)
            client.service_providers.add(sub_service.service.service_provider)
            client.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class SubServiceCreateAPIView(generics.CreateAPIView):
    serializer_class = my_serializers.SubServiceSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

