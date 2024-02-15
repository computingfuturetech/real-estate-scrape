from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime, timedelta

class User(AbstractUser):
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=11,null=True, blank=True,)
    date_of_birth=models.DateField(null=True, blank=True,)
    def __str__(self):
        return self.username
    


class EmailOtp(models.Model):
    email=models.ForeignKey(User,on_delete=models.CASCADE)
    otp=models.CharField(max_length=6)
    expiration_time = models.DateTimeField(default=timezone.now() + timedelta(minutes=2))

    def __str__(self):
        return f"OTP for {self.email}"
