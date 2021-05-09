from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from customer.models import Customer


from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.conf import settings

import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image,ImageDraw


# Create your models here.

GENDER_CHOICES = (
    ("Male","Male"),
    ("Female","Female"),
    ("Other","Other"),
)

class User(AbstractUser):
    
    is_admin=models.BooleanField(default=False)
    is_customer=models.BooleanField(default=False)



@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "Dear Customer, \n Your Password reset link is : {}?token={}. \n Note: Please Don't reply to this mail. \n Regards H2O GYM ".format("https://www.health2offer.com/reset-password/", reset_password_token.key)
    email_from = settings.EMAIL_HOST_USER
    send_mail(
        # title:
        "Password Reset for {title}".format(title="attendance"),
        # message:
        email_plaintext_message,
        # from:
        email_from,
        # to:
        [reset_password_token.user.email]
    )

class PresentQrCode(models.Model):
    name = models.CharField(max_length=200)
    qr_code = models.ImageField(upload_to='qr_codes',blank=True)

    def __str__(self):
        return str(self.id)




    def save(self,*args,**kwargs):
        qrcode_img = qrcode.make(self.name)
        canvas = Image.new('RGB',(300,300),'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname =f'qr_code_{self.name}'+'.png'
        buffer =BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname, File(buffer) , save=False)
        canvas.close()
        super().save(*args,**kwargs)
# Create your models here.
