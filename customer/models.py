from django.db import models

# from core.models import User
import datetime
# from trainer.models import *
# Create your models here.

GENDER_CHOICES = (
    ("Male","Male"),
    ("Female","Female"),
    ("Other","Other"),
)


ID_PROOF_CHOICES = (
    ("Aadhar Card","Aadhar Card"),
    ("Pan Card","Pan Card"),
    ("Driving License","Driving License"),
    ("Voter ID","Voter ID"),
)


# Create your models here.

class Customer(models.Model):
    user = models.ForeignKey('core.User',on_delete=models.CASCADE,null=True,blank=True)
    first_name=models.CharField(max_length=100)
    middle_name=models.CharField(max_length=100,null=True,blank=True)
    last_name=models.CharField(max_length=100,null=True,blank=True)
    date_of_birth=models.DateField(default="2000-02-01",null=True,blank=True)
    gender=models.CharField(choices=GENDER_CHOICES,max_length=30,default="Male")
    phone=models.CharField(max_length=12,null=True)
    alternate_phone=models.CharField(max_length=12,null=True,blank=True)
    email=models.EmailField()
    address1=models.CharField(max_length=200,default=" ",blank=True)
    address2=models.CharField(max_length=200,default=" ",blank=True)
    city=models.CharField(max_length=50,null=True,blank=True)
    state=models.CharField(max_length=50,null=True,blank=True)
    pincode=models.IntegerField(default=0,null=True,blank=True)
    photo=models.ImageField(upload_to="customer/photo/",blank=True)
    id_proof=models.CharField(max_length=100,choices=ID_PROOF_CHOICES,default="N/A")
    id_proof_image=models.ImageField(upload_to='customer/idproof/',blank=True,)
    id_proof_image1=models.ImageField(upload_to='customer/idproof/',blank=True,)
    active = models.BooleanField(default=True)
    date_added=models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + " " + self.first_name


class CustomerAttendance(models.Model):
    
    customer=models.ForeignKey(Customer, on_delete=models.PROTECT)
    date=models.DateField(auto_now_add=True)
    check_in_time = models.TimeField(auto_now_add=True, null=True,blank=True)
    check_out_time=models.TimeField(null=True, blank=True)
    present=models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.customer.id) + " " + self.customer.first_name +  " " + str(self.date)
        
    class Meta:
        verbose_name_plural = 'Customer Attendance'

