from django.urls import path
import api.views as apis


urlpatterns = [
    path('login', apis.LoginAPIView.as_view()),
    path('signup/sp', apis.ServiceProviderSignUpAPIView.as_view()),
    path('signup/client', apis.ClientSignUpAPIView.as_view()),
    path('client/<uuid:client_id>', apis.ClientDataRetrieveAPIView.as_view()),
    path('client/update', apis.ClientUpdateAPIView.as_view()),
    path('sp/<uuid:sp_id>', apis.ServiceProviderDataRetrieveAPIView.as_view()),
    path('sp/update', apis.ServiceProviderUpdateAPIView.as_view()),
    path('service/create', apis.ServiceCreateAPIView.as_view()),
    path('service/update', apis.ServiceUpdateAPIView.as_view()),
    path('service/list', apis.ServiceListAPIView.as_view()),
    path('subservice/create', apis.SubServiceCreateAPIView.as_view()),
    path('service/<uuid:service_id>', apis.ServiceDataRetrieveAPIView.as_view()),
]