from .models import User,EmailOtp
from rest_framework import generics,status
from .serializers import UserCreateSerializer,ChangePasswordserializer,UserUpdateSerializer,UserTwoFactorAuthenticationSerializer
from .permissions import IsOwnerOrAdmin
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate,login
from rest_framework_simplejwt.tokens import RefreshToken
import random
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework.views import APIView
import os
from django.utils import timezone
from datetime import timedelta




class UserCreateViewSet(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserCreateSerializer
    permission_classes = [IsOwnerOrAdmin]

    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get('username')
            email = request.data.get('email')
            exist_username = User.objects.filter(username=username).exists()
            exist_email = User.objects.filter(email=email).exists()               
            if exist_username:
                return Response({'status': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)               
            if exist_email:
                return Response({'status': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({'status': 'User created successfully'}, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@api_view(['POST'])
@permission_classes([])
def login_view(request):
    if request.method == 'POST':
        email_or_username = request.data.get('email')
        password = request.data.get('password')

        if not email_or_username or not password:
            return Response({'error': 'Please provide both email or username and password.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if '@' in email_or_username:
            user = authenticate(request, email=email_or_username, password=password)
        else:
            user = authenticate(request, username=email_or_username, password=password)

        if user is not None:
            if user.twofa:
                otp = str(random.randint(100000, 999999))
                EmailOtp.objects.filter(email=user.id).delete()
                emaill = User.objects.get(email=user.email)
                EmailOtp.objects.create(email=emaill, otp=otp)
                send_mail(
                    'Your OTP',
                    f'Your OTP is: {otp}',
                    settings.EMAIL_HOST_USER, 
                    [user.sec_email],  
                    fail_silently=False,
                )
                return Response({'status': 'OTP sent successfully'}, status=status.HTTP_201_CREATED)
            else:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                response_data = {
                    'token': access_token,
                    'user_id': user.id,
                    'status':'Successfully login',
                }
                return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ChangePasswordViewSet(generics.UpdateAPIView):
    queryset=User.objects.all()
    serializer_class=ChangePasswordserializer
    permission_classes=[IsOwnerOrAdmin]

    def put(self, request, *args, **kwargs):
        user=self.request.user
        instance=User.objects.filter(pk=user.id)
        serializer=self.get_serializer(instance,data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data={
                'status':'Successfully Change password'
            }
            return Response(response_data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class SendOtpToUser(generics.CreateAPIView):
    
    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            exist_email = User.objects.filter(email=email)                           
            if exist_email:
                emaill = User.objects.get(email=email)
                otp = str(random.randint(100000, 999999))
                EmailOtp.objects.filter(email=emaill.id).delete()
                current_time = timezone.localtime()
                new_time = current_time + timedelta(minutes=5)
                time_string = new_time.strftime('%H:%M:%S')
                write=EmailOtp.objects.create(email=emaill,otp=otp,expiration_time=time_string)
                if write:
                    send_mail(
                    'Your OTP',
                    f'Your OTP is: {otp}',
                    settings.EMAIL_HOST_USER, 
                    [email],  
                    fail_silently=False,
                    )
                return Response({'status': 'OTP send successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Invalid Email'}, status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ForgetPassword(generics.UpdateAPIView):
    def put(self, request, *args, **kwargs):
        email = request.data.get('email')
        new_password = request.data.get('password')
        if not email or not new_password:
            return Response({'error':('Please provide both email and password.')}, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_email(email)
        except ValidationError:
            return Response({'error': ('Invalid email address.')}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': ('User with this email does not exist.')}, status=status.HTTP_404_NOT_FOUND)
        user.set_password(new_password)
        user.save()
        emaill = User.objects.get(email=email)
        EmailOtp.objects.filter(email=emaill.id).delete()
        return Response({'status': ('Password updated successfully.')}, status=status.HTTP_200_OK)


class VerifyOTP(APIView):
    def post(self, request):
        otp_entered = request.data.get('otp')
        email = request.data.get('email')
        if not email or not otp_entered:
            return Response({'error':('Please provide both email and OTP.')}, status=status.HTTP_400_BAD_REQUEST)
        user_email=User.objects.get(email=email)
        if user_email:
            otp_object = EmailOtp.objects.filter(email=user_email)
            if otp_object:
                otp_objectt = EmailOtp.objects.get(email=user_email)
                if otp_objectt.otp == otp_entered:
                    otp_objectt.delete()
                    return Response({'message': 'OTP verified successfully.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'OTP not Found.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'user email not found.'}, status=status.HTTP_400_BAD_REQUEST)

def delete_user_image(instance):
    if instance.image:

        image_path = instance.image.path
        instance.image.delete()
        if os.path.isfile(image_path):
            os.remove(image_path)

@api_view(['POST'])
def update_user(request):
    if request.method == 'POST':
        try:
            user = request.user
            instance = User.objects.get(pk=user.id)
            if not request.data:
                serializer = UserUpdateSerializer(instance)
                response_data = serializer.data
                response_data['email'] = instance.email
                return Response(response_data)
            if 'image' in request.data:
                if instance.image:
                    instance.image.delete()
                instance.image = request.data['image']

            serializer = UserUpdateSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response_data = serializer.data
                response_data['email'] = instance.email
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def add_twofa(request):
    if request.method == 'POST':
        try:
            user = request.user
            instance = User.objects.get(pk=user.id)
            if not request.data:
                serializer = UserTwoFactorAuthenticationSerializer(instance)
                return Response(serializer.data)
            if 'twofa' in request.data:
                twofa_enabled = request.data.get('twofa')
                if twofa_enabled=='True':
                    sec_email = request.data.get('sec_email')
                    if not sec_email:
                        return Response({'error': 'Secondary email is required to enable two-factor authentication'}, status=status.HTTP_400_BAD_REQUEST)
                    instance.sec_email = sec_email
                    instance.twofa = True
                    instance.save()
                    serializer = UserTwoFactorAuthenticationSerializer(instance)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                if twofa_enabled == 'False':
                    instance.sec_email= None
                    instance.twofa = twofa_enabled
                    instance.save()
                    return Response({'message': 'Two-factor authentication disabled successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'The "twofa" field is required'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class VerifyOTPForTwoFactorauthentication(APIView):
    def post(self, request):
        otp_entered = request.data.get('otp')
        email = request.data.get('email')
        if not otp_entered or not email:
            return Response({'error':('Please provide both email and otp.')}, status=status.HTTP_400_BAD_REQUEST)
        user_email = User.objects.get(email=email)
        try:
            otp_object = EmailOtp.objects.get(email=user_email)
        except:
            return Response({'error': 'Time Expire.'}, status=status.HTTP_400_BAD_REQUEST)
        if otp_object.otp == otp_entered:
            user = User.objects.get(email=email)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            response_data = {
                'token': access_token,
                'user_id': user.id,
                'status': 'Successfully logged in'
            }
            otp_object.delete()
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
