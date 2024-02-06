from django.urls import path,include
from user import views

urlpatterns=[
    path('create/',views.UserCreateViewSet.as_view(),name='user-creation'),
    path('login/',views.login_view,name='login'),
    path('cpassword/',views.ChangePasswordViewSet.as_view(),name='change_password'),
]
