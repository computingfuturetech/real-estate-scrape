from rest_framework import serializers
from djoser.serializers import UserSerializer as BaseUserSerializer,UserCreateSerializer as BaseUserCreateSerializer
from django.contrib.auth.password_validation import validate_password
from .models import User
from django.conf import settings

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields=['username','password','email','first_name','last_name','phone','bio']

class ChangePasswordserializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Incorrect old password")
        return value

    def validate(self, data):
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError("New password must be different from the old password")
        return data

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()


class ForgetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['first_name','last_name','phone','bio','image']
    

class UserTwoFactorAuthenticationSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['twofa','sec_email']      
