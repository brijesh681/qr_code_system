from . import models
from rest_framework import serializers
from datetime import datetime, timedelta, date



class CustomerSerializer(serializers.ModelSerializer):
    # custid = serializers.SerializerMethodField(read_only=True)
    # batch_time_to = serializers.SerializerMethodField(read_only=True)
    # batch_time_from = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=models.Customer
        fields='__all__'


    # def get_batch_time_to(self, obj):
    #     # cust = models.Customer.objects.get(user=obj.user)
    #     return obj.batch_id.batch_time_to
    #
    # def get_batch_time_from(self, obj):
    #     # cust = models.Customer.objects.get(user=obj.customer.user)
    #     return obj.batch_id.batch_time_from

class CustomerListSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Customer
        fields='__all__'
class CustomerAttendanceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=models.CustomerAttendance
        exclude=('date',)
        depth=1


class MarkAttendanceSerializer(serializers.ModelSerializer):
    date=serializers.ReadOnlyField()
    class Meta:
        model=models.CustomerAttendance
        fields=('check_in_time','check_out_time','date','present')


class AttendanceReportSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=models.CustomerAttendance
        fields=('date','present','customer')

class CustomerProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=models.Customer
        exclude = ('active')