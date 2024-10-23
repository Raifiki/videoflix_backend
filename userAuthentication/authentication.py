from django.contrib.auth.backends import ModelBackend
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator

class LoginCustomUserAuthentication(BaseAuthentication):
    """ This class is used to authenticate the user """
    def authenticate(self, request):
        """ This methode is used to authenticate the user, there are four possible return values:
        1. User does not exist
        2. Invalid password
        3. User is not active
        4. User is authenticated"""
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return None
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('User does not exist')

        if not user.check_password(password):
            raise AuthenticationFailed('Invalid password')
        
        if not user.is_active:
            raise AuthenticationFailed('email adress not verified')

        return (user, None)

class EmailVerificationAuthentication(BaseAuthentication):
    """ This class is used to verify the email address of the user by token authentication. There are three possible return values:
    1. User does not exist
    2. Token is invalid
    3. Email is verified"""
    def authenticate(self, request):
        user_id = request.query_params.get('user_id')
        token = request.query_params.get('token')
        if not user_id or not token:
            return None
        try:
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('User does not exist')
        if not default_token_generator.check_token(user, token):
            raise AuthenticationFailed('token is invalid')
        return (user, None)

class ResetPasswordTokenAuthentication(BaseAuthentication):
    """ This class is used to authenticate the user by token authentication for reset password. There are four possible return values:
    1. User does not exist
    2. Email is not verified
    3. Token is invalid
    4. User is authenticated"""
    def authenticate(self, request):
        user_id = request.query_params.get('user_id')
        token = request.query_params.get('token')
        if not user_id or not token:
            return None
        try:
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('User does not exist')
        if not user.is_active:
            raise AuthenticationFailed('email adress not verified')
        token_generator=PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            raise AuthenticationFailed('token is invalid or expired')
        return (user, None)