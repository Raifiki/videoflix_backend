from django.contrib.auth.backends import ModelBackend
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator

class LoginCustomUserAuthentication(BaseAuthentication):
    def authenticate(self, request):
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