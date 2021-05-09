from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .serializers import *

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from datetime import datetime, timedelta,date

from customer.models import Customer,CustomerAttendance
from rest_framework.permissions import IsAuthenticated
from customer.serializers import CustomerSerializer,MarkAttendanceSerializer


from rest_framework.parsers import JSONParser

import re
from .models import PresentQrCode
import io
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
csrf_exempt
class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    #permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#-------------------------------------------------------------check----------------------------------------------------

class QrCodeCustomerAPIView(generics.CreateAPIView):
    queryset = CustomerAttendance.objects.all()
    serializer_class = MarkAttendanceSerializer 
   #permission_classes = [permissions.IsAuthenticated, ]

    def create(self,request,*args,**kwargs):
        if request.method=='POST':
            json_data = request.body
            print(json_data)
            stream = io.BytesIO(json_data)
            print(stream)
            secret_key2 = JSONParser().parse(stream)
            key=str(tuple(secret_key2))
            key = " ".join(re.split("[^a-zA-Z]",key))
            print(key)
            secret_key2=str(key).strip()
            crd = PresentQrCode.objects.values_list('name')
            print("return:",crd)
            brd = str(tuple(crd))
            zid = " ".join(re.split("[^a-zA-Z]",brd))
            secret_key1=str(zid).strip()
            print(type(secret_key1))
            print("Return:",secret_key1)
            print("Return:",secret_key2)
            if secret_key1 == secret_key2:
                print("valid user")
                if not(request.user.is_admin or request.user.is_customer ):
                    return Response({"NO_ACCESS": "Access Denied"}, status=401)
                if request.user.is_customer:
                    customer=Customer.objects.get(id=self.kwargs["id"])
                    serializer = MarkAttendanceSerializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save(customer=customer,present=True)
                    return Response(serializer.data,status=201)          
            else:            
                return Response({"NO_ACCESS": "Access Denied"}, status=401)          
        
        


   

            
