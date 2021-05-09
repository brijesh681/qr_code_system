from django.urls import path,include
from .views import *

urlpatterns = [
    path('QRCodeCustomer/<int:id>/', QrCodeCustomerAPIView.as_view()),
   
    path('rest-auth/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('rest-auth/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]