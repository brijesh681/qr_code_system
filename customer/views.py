from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework import status, permissions
from django.shortcuts import redirect
from rest_framework.response import Response
from .filter import CustomerFilter, AttendanceFilter
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework.pagination import PageNumberPagination
from core.models import User
from datetime import datetime, timedelta,date
from django.db.models import Q
from rest_framework import viewsets


class CustomerAPIView(generics.CreateAPIView):

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    #permission_classes = [permissions.IsAuthenticated, ]

    def create(self,request,*args,**kwargs):

        if not(request.user.is_admin ):
            
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
     

        phone=request.data['phone']
        print(phone)
        try:
            user=User.objects.create_user(username=phone,password=phone,email=request.data['email'],is_customer=True)
        except IntegrityError:
            return Response({"USER_EXISTS":"User already exists with this phone number"},status=400)

        # request.data['user'] = user.id
        print(request.data)
        # if request.data['address1'] == 'null' or request.data['address1'] == None or request.data['address1'] == 'NULL':
        #     request.data['address1'] = ' '
        # if request.data['address2'] == 'null' or request.data['address2'] == None or request.data['address2'] == 'NULL':
        #     request.data['address2'] = ' '
        serializer = CustomerSerializer(data=request.data)
    
        if serializer.is_valid():
            # Customer.objects.create(user=user.id,first_Name=)
            serializer.save(user=user)
            return Response(serializer.data, status=201)
        else:
            u=User.objects.filter(username=phone,email=request.data['email'],is_customer=True)
            if u.exists():
                u.delete()
            return Response(serializer.errors, status=400)

class EmailChange(APIView):
    #permission_classes = [permissions.IsAuthenticated, ]
    def post(self,request,*args,**kwargs):
        try:
            instance = Customer.objects.get(id=self.kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"DOES_NOT_EXIST":"Does not exist"},status=400)
        user = User.objects.get(id=instance.user.id)
        user.email = request.data['email']
        user.save()
        return Response("Email Id Changed",status=200)


class TodayPresentAttendanceAPIView(generics.ListAPIView):
    
    queryset=CustomerAttendance.objects.filter(date=datetime.now().date(),customer__active=True,present=True)
    serializer_class=CustomerAttendanceSerializer
    #permission_classes = [permissions.IsAuthenticated, ]

    def list(self, request, *args, **kwargs):

        if not(request.user.is_admin ):
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
      

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)


class TodayAbsentAttendanceAPIView(generics.ListAPIView):
    
    queryset=CustomerAttendance.objects.filter(date=datetime.now().date(),customer__active=True,present=False)
    serializer_class=CustomerAttendanceSerializer
    #permission_classes = [permissions.IsAuthenticated, ]

    def list(self, request, *args, **kwargs):

        if not(request.user.is_admin ):
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
      
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)


class MarkPresentAPIView(generics.CreateAPIView):
    
    queryset = CustomerAttendance.objects.all()
    serializer_class = MarkAttendanceSerializer
    #permission_classes = [permissions.IsAuthenticated, ]
    
    def create(self,request,*args,**kwargs):

        if not(request.user.is_admin ):
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
    
        
        customer=Customer.objects.get(id=self.kwargs["id"])
        serializer = MarkAttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=customer,present=True,date=datetime.now().date())
        return Response(serializer.data,status=201)


class MarkAbsentAPIView(generics.ListAPIView):
    
    #permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = AttendanceReportSerializer
    
    def list(self,request,*args,**kwargs):

        if not(request.user.is_admin ):
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
     
        
        customer=Customer.objects.get(id=self.kwargs["id"])
        obj=CustomerAttendance.objects.create(customer=customer,present=False,date=datetime.now().date())
        obj.save()
        
        return Response({"SUCCESS":"success"},status=201)


class AttendanceReportAPIView(generics.ListAPIView):
    
    queryset = CustomerAttendance.objects.all()
    serializer_class = AttendanceReportSerializer
    #permission_classes = [permissions.IsAuthenticated, ]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AttendanceFilter
    
    def list(self, request,*args,**kwargs):

        if not(request.user.is_admin ):
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
 
        
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        queryset=queryset.filter(customer__active=True)
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data,status=200)



class AttendanceOfCustomer(generics.ListAPIView):

    queryset = CustomerAttendance.objects.all()
    serializer_class = CustomerAttendanceSerializer
    #permission_classes = [permissions.IsAuthenticated, ]
    

    def list(self, request, *args, **kwargs):
        customer = Customer.objects.get(id=self.kwargs["id"])
        #print(customer)
        today=datetime.now().date()
        month=today.month
        year=today.year
        queryset = self.queryset.filter(customer=customer,present=True,date__year=year,date__month=month)
        
        l = []
        if queryset.count()==0:
            # print(l)
            return Response({"list": l,"percentage":0},status=200)

        queryset = queryset.order_by('date')
        a = queryset[0].date
        ch=0
        i=0
        b = queryset[0].date
        for i in range(b.day-1,0,-1):
            x = timedelta(days=i)
            # print(i)
            l.append([b-x, "False"])
        i=0

        while(a<=queryset[queryset.count()-1].date):
            if i<0:
                break
            if a == queryset[i].date:
                l.append([a, "True"])
                i+=1
            else:
                l.append([a, "False"])
            t = timedelta(days=1)
            a = a + t

        # print(l)
        days_present=0
        for i in l:
            if i[1]=="True":
                days_present+=1
        
        if len(l):
            percentage=round((days_present/len(l))*100,2)
        else:
            percentage=0

        print(percentage)
        return Response({"list": l,"percentage":percentage},status=200)



class MyAttendanceCustomer(generics.ListAPIView):

    queryset = CustomerAttendance.objects.all()
    serializer_class = CustomerAttendanceSerializer
    #permission_classes = [permissions.IsAuthenticated, ]
    
    def list(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        #print(customer)
        today=datetime.now().date()
        month=today.month
        year=today.year
        queryset = self.queryset.filter(customer=customer,present=True,date__year=year,date__month=month)
        
        l = []
        if queryset.count()==0:
            # print(l)
            return Response({"list": l,"percentage":0},status=200)

        queryset = queryset.order_by('date')
        a = queryset[0].date
        ch=0
        i=0
        b = queryset[0].date
        for i in range(b.day-1,0,-1):
            x = timedelta(days=i)
            # print(i)
            l.append([b-x, "False"])
        i=0

        while(a<=queryset[queryset.count()-1].date):
            if i<0:
                break
            if a == queryset[i].date:
                l.append([a, "True"])
                i+=1
            else:
                l.append([a, "False"])
            t = timedelta(days=1)
            a = a + t

        # print(l)
        days_present=0
        for i in l:
            if i[1]=="True":
                days_present+=1
        
        if len(l):
            percentage=round((days_present/len(l))*100,2)
        else:
            percentage=0

        print(percentage)
        return Response({"list": l,"percentage":percentage,"total_attendance_numerator":days_present,"total_attendance_denominator":len(l),},status=200)

class UserDeleteAPI(APIView):
    #permission_classes = [permissions.IsAuthenticated, ]
    def post(self,request):
        if not (request.user.is_admin ):
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
   
        cust=Customer.objects.get(id=request.data['cust_id'])
        user=User.objects.get(id=cust.user.id)
        cust.delete()
        user.delete()
        return Response("Account Deleted",status=200)

class CustomerInactive(APIView):
    #permission_classes = [permissions.IsAuthenticated, ]
    def post(self,request):
        if not (request.user.is_admin ):
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
     
        cust=Customer.objects.get(id=request.data['cust_id'])
        if cust.active == True:
            cust.active = False
        else:
            cust.active = True
        cust.save()
        return Response("Account Inactive",status=200)
class CustomerAPIListView(generics.ListAPIView):

    queryset=Customer.objects.all().order_by('first_name')
    serializer_class=CustomerListSerializer
    #permission_classes = [permissions.IsAuthenticated, ]
    search_fields=['first_name','middle_name','last_name','phone','email','alternate_phone']
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = CustomerFilter
 
    def list(self, request, *args, **kwargs):

        if not(request.user.is_admin ):
            
            return Response({"NO_ACCESS": "Access Denied"}, status=401)


        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)


class CustomerAPIUpdateView(generics.RetrieveUpdateAPIView):

    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer
    #permission_classes = [permissions.IsAuthenticated, ]
    lookup_field='id'

    def retrieve(self,request,*args,**kwargs):

        if not(request.user.is_admin ):
            
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
    
        try:
            instance = self.queryset.get(id=self.kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"DOES_NOT_EXIST":"Does not exist"},status=400)
        
        serializer = self.get_serializer(instance)

        return Response(serializer.data,status=200)

    def partial_update(self,request,*args,**kwargs):

        if not(request.user.is_admin ):
            
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
        

        try:
            instance = self.queryset.get(id=self.kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"DOES_NOT_EXIST":"Does not exist"},status=400)
        
        serializer = self.get_serializer(instance,data=request.data,partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(request.data['email'])
        print(instance.user.email)
        user = User.objects.get(id=instance.user.id)
        user.email = request.data['email']
        user.save()
        return Response(serializer.data,status=200)


class CustomerProfileAPIView(APIView):
    #permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request,*args,**kwargs):
        try:
            inst = models.Customer.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return Response("Id Doesn't Exists", status=404)
        serializer = CustomerProfileSerializer(inst)
        return Response(serializer.data,status=200)