from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=11)
    date_of_birth=models.DateField(null=True, blank=True,)
    def __str__(self):
        return self.username
