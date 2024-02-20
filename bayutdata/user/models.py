from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime, timedelta
import re,os


def user_image_path(instance, filename):
    user_id = instance.id
    _, file_extension = os.path.splitext(filename)
    new_filename = f"{user_id}pfp{file_extension}"
    return os.path.join('store/images', new_filename)



class User(AbstractUser):
    email=models.EmailField(unique=True)
    sec_email=models.EmailField(blank=True, null=True)
    phone=models.CharField(max_length=11,null=True, blank=True,)
    image = models.ImageField(upload_to=user_image_path, blank=True, null=True)
    bio=models.CharField(max_length=1000,blank=True, null=True)
    twofa=models.BooleanField(default=False)
    def __str__(self):
        return self.username
    


class EmailOtp(models.Model):
    email=models.ForeignKey(User,on_delete=models.CASCADE)
    otp=models.CharField(max_length=6)
    expiration_time = models.DateTimeField(default=timezone.now() + timedelta(minutes=2))

    def __str__(self):
        return f"OTP for {self.email}"
    



