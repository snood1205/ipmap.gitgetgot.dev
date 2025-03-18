from django.urls import path
from .views import WhoisIpView

urlpatterns = [
    path('whois_ip/', WhoisIpView.as_view(), name='whois_ip'),
]
