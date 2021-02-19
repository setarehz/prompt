from django.urls import path
import api.views as apis


urlpatterns = [
    path('login', apis.LoginAPIView.as_view()),
    path('signup', apis.SignUpAPIView.as_view()),
    path('getuserdata', apis.UserDataRetrieveAPIView.as_view()),
    path('getclientdata', apis.ClientDataRetrieveAPIView.as_view()),
    path('getspdata', apis.ServiceProviderDataRetrieveAPIView.as_view()),
    path('sp_update', apis.ServiceProviderUpdateAPIView.as_view()),
    path('client_update', apis.ClientUpdateAPIView.as_view()),
    path('create_service', apis.ServiceCreateAPIView.as_view()),
    path('update_service', apis.ServiceUpdateAPIView.as_view()),
    path('services_list', apis.ServiceListAPIView.as_view())
]