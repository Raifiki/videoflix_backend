from rest_framework import serializers
from rest_framework.authtoken.models import Token
from userAuthentication.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email','password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['token'] = Token.objects.get(user=instance).key
        return data


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email not found')
        return value
 
class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=128)
    new_passwordConfirm = serializers.CharField(max_length=128)
    def validate(self, data):
        if data['new_password'] != data['new_passwordConfirm']:
            raise serializers.ValidationError('Passwords do not match')
        return data
    
class CreateCustomUserSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField(max_length=128)
        passwordConfirm = serializers.CharField(max_length=128)
        def validate(self, data):
            if data['password'] != data['passwordConfirm']:
                raise serializers.ValidationError('Passwords do not match')
            if CustomUser.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError('Email already exists')
            return data