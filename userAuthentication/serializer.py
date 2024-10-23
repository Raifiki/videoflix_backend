from rest_framework import serializers
from rest_framework.authtoken.models import Token
from userAuthentication.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    """ Serializer for CustomUser model """
    class Meta:
        model = CustomUser
        fields = ['id','email','password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def to_representation(self, instance):
        """Function to add token to the response """
        data = super().to_representation(instance)
        data['token'] = Token.objects.get(user=instance).key
        return data


class PasswordResetSerializer(serializers.Serializer):
    """ Serializer for password reset """
    email = serializers.EmailField()

    def validate_email(self, value):
        """ Validate email exists in database """
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email not found')
        return value
 
class PasswordResetConfirmSerializer(serializers.Serializer):
    """ Serializer for password reset confirmation """
    new_password = serializers.CharField(max_length=128)
    new_passwordConfirm = serializers.CharField(max_length=128)
    def validate(self, data):
        """ Validate new password and confirm password match """
        if data['new_password'] != data['new_passwordConfirm']:
            raise serializers.ValidationError('Passwords do not match')
        return data
    
class CreateCustomUserSerializer(serializers.Serializer):
        """ Serializer for creating a new user """
        email = serializers.EmailField()
        password = serializers.CharField(max_length=128)
        passwordConfirm = serializers.CharField(max_length=128)
        def validate(self, data):
            """ Validate password and confirm password match and email already exists """
            if data['password'] != data['passwordConfirm']:
                raise serializers.ValidationError('Passwords do not match')
            if CustomUser.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError('Email already exists')
            return data