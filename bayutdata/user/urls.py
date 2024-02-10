from django.urls import path,include
from user import views

urlpatterns=[
    path('create/',views.UserCreateViewSet.as_view(),name='user-creation'),
    path('login/',views.login_view,name='login'),
    path('cpassword/',views.ChangePasswordViewSet.as_view(),name='change_password'),
    path('send-otp/', views.SendOtpToUser.as_view(), name='send_otp'),
    path('forget-password/', views.ForgetPassword.as_view(), name='send_otp'),
    path('verify-otp/', views.VerifyOTP.as_view(), name='verify-otp'),
]
