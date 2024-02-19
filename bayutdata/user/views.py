from django.shortcuts import render
from .models import User,EmailOtp
from rest_framework import generics,status
from .serializers import UserCreateSerializer,ChangePasswordserializer,UserProfileSerializer,UserUpdateSerializer,UserTwoFactorAuthenticationSerializer
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
from django.core.exceptions import PermissionDenied


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
        

# @api_view(['POST'])
# @permission_classes([])
# def login_view(request):
#     if request.method == 'POST':
#         email_or_username = request.data.get('email')
#         password = request.data.get('password')

#         if not email_or_username or not password:
#             return Response({'error':('Please provide both email or username and password.')}, status=status.HTTP_400_BAD_REQUEST)
        
#         if '@' in email_or_username:
#             user = authenticate(request, email=email_or_username , password=password)
#         else:
#             user = authenticate(request, username=email_or_username , password=password)

#         if user is not None:
#             check_two_factor_authentication=User.objects.get(email_or_username=email_or_username)
#             if check_two_factor_authentication.twofa == True:
#                 exist_email = User.objects.filter(email_or_username=email_or_username)                           
#                 if exist_email:
#                     emaill = User.objects.get(email=email_or_username)
#                     otp = str(random.randint(100000, 999999))
#                     EmailOtp.objects.filter(email=emaill.id).delete()
#                     write=EmailOtp.objects.create(email=emaill,otp=otp)
#                     if write:
#                         send_mail(
#                         'Your OTP',
#                         f'Your OTP is: {otp}',
#                         settings.EMAIL_HOST_USER, 
#                         [emaill.email],  
#                         fail_silently=False,
#                         )
#                     return Response({'status': 'OTP send successfully'}, status=status.HTTP_201_CREATED)
#                 else:
#                     return Response({'error': 'Invalid Email'}, status=status.HTTP_401_UNAUTHORIZED)

#             # login(request, user)

#             # refresh = RefreshToken.for_user(user)
#             # access_token = str(refresh.access_token)
#             # response_data = {
#             #     'token': access_token,
#             #     'user_id': user.id,
#             #     'status':'Successfully login',
#             # }
#             # return Response(response_data, status=status.HTTP_200_OK)
#         # else:
#         #     return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#     else:
#         return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

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
                    [user.email],  
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
                 
                write=EmailOtp.objects.create(email=emaill,otp=otp)
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
        user_email=User.objects.get(email=email)
        otp_object = EmailOtp.objects.get(email=user_email)
        if not otp_entered or not email:
            return Response({'error':('Please provide both email and otp.')}, status=status.HTTP_400_BAD_REQUEST)
        if otp_object.otp == otp_entered:
            otp_object.delete()
            return Response({'message': 'OTP verified successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserProfileViewSet(generics.RetrieveUpdateAPIView):
    queryset=User.objects.all()
    serializer_class=UserProfileSerializer
    permission_classes=[IsOwnerOrAdmin]

    def get(self, request, *args, **kwargs):
        user=self.request.user
        try:
            instance = User.objects.get(pk=user.id)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, *args, **kwargs):
        user = self.request.user
        try:
            instance = User.objects.get(pk=user.id)
            if instance.image:
                instance.image.delete()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                if serializer.validated_data:
                    serializer.save()
                    return Response({'status': 'Profile updated successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'No changes detected'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class UpdateUserViewSet(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes=[IsOwnerOrAdmin]
    def get_object(self):
        user = self.request.user
        if hasattr(user, 'id'):
            return user
        else:
            raise PermissionDenied('Unauthorized: User not found or authenticated')
    def patch(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            serializer = self.get_serializer(instance=user, data=request.data, partial=True)
            provided_fields = set(request.data.keys())
            serializer_fields = set(serializer.fields.keys())
            if not provided_fields.issubset(serializer_fields):
                missing_fields = provided_fields - serializer_fields
                return Response(
                    {'error': f'The following fields are not allowed to be updated: {", ".join(missing_fields)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if serializer.is_valid():
                serializer.save()
                response_data = {
                        'status': 'Successfully Updated'
                    }
                return Response(response_data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

class TwoFactorAuthenticationViewSet(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserTwoFactorAuthenticationSerializer
    permission_classes=[IsOwnerOrAdmin]
    def get_object(self):
        user = self.request.user
        if hasattr(user, 'id'):
            return user
        else:
            raise PermissionDenied('Unauthorized: User not found or authenticated')
    def patch(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            serializer = self.get_serializer(instance=user, data=request.data, partial=True)
            provided_fields = set(request.data.keys())
            serializer_fields = set(serializer.fields.keys())
            if not provided_fields.issubset(serializer_fields):
                missing_fields = provided_fields - serializer_fields
                return Response(
                    {'error': f'The following fields are not allowed to be updated: {", ".join(missing_fields)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if serializer.is_valid():
                serializer.save()
                response_data = {
                        'status': 'Successfully Updated'
                    }
                return Response(response_data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        

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