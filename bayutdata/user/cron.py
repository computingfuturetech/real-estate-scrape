from .models import EmailOtp
from datetime import datetime, timedelta
from django.utils import timezone

def delete_otp():
    current_time = timezone.now()
    EmailOtp.objects.filter(expiration_time__lt=current_time).delete()
