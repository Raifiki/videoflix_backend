from urllib import request
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
#imports for rest framework
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from userAuthentication.models import CustomUser
from userAuthentication.serializer import CustomUserSerializer, PasswordResetConfirmSerializer, PasswordResetSerializer
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator

from django.core.mail import send_mail
from django.template.loader import render_to_string

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = []#[TokenAuthentication]
    
    def create(self, request, *args, **kwargs):
        if not self.validateData(request.data): return HttpResponse('Missing data', status=400)
        email, password, passwordConfirm = self.getData(request.data)
        if password != passwordConfirm: return HttpResponse('Passwords do not match', status=400)
        if CustomUser.objects.filter(email=email).exists(): return HttpResponse('Email already exists', status=400)
        user = CustomUser.objects.create_user(email, password)
        respData = CustomUserSerializer(user).data
        return  Response(respData, content_type='application/json')
    
    def validateData(self, data):
        return data.get('email') and data.get('password') and data.get('passwordConfirm')
    
    def getData(self, data):
        email = data.get('email')
        password = data.get('password')
        passwordConfirm = data.get('passwordConfirm')
        return email, password, passwordConfirm
    
class VerifyEmailView(View):
    def get(self, request,user_id, token):
        try:
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return HttpResponse('Invalid user', status=400)
        if not default_token_generator.check_token(user, token):
            return HttpResponse('Invalid token', status=400)
        user.is_active = True
        user.save()
        return HttpResponse('Email verified', status=200)
    
class LoginView(ObtainAuthToken):
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            respData = CustomUserSerializer(user).data
            return Response(respData, content_type='application/json')
        return Response('Invalid Data',status=400)
    
class ResetPasswordView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            self._send_password_reset_email(email)
            return Response({'message': 'Password reset email sent'}, status=200)
        return Response(serializer.errors, status=400)
    
    def _send_password_reset_email(self, email):
        user = CustomUser.objects.get(email=email)
        mail = 'leonard_weiss@web.de'# ToDo: change email to: instance.email
        from_mail = 'django@demomailtrap.com' # ToDo: change email to domain email
        token_generator=PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        subject = 'Reset your Password'
        
        context = {
            'username': mail.split('@')[0],
            'reset_pwd_url': 'http://localhost:4200/ResetPassword/?user_id=' + str(user.pk) + '&token=' + token
        }
        text_content = 'Please reset your password'
        html_content = render_to_string('reset_pwd_email.html', context)
      
        send_mail(subject, text_content, from_mail, [mail], html_message=html_content)
        
class ResetPasswordConfirmView(APIView):
    def post(self, request, user_id, token):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            #ToDo make authentication with token - start
            try:
                user = CustomUser.objects.get(pk=user_id)
            except CustomUser.DoesNotExist:
                return Response('User does not exist',status=400)
            token_generator=PasswordResetTokenGenerator()
            if not token_generator.check_token(user, token):
                return Response('token us invalid or expired',status=400)
            if not user.is_active:
                return Response('email adress not verified',status=400)
            #ToDo make authentication with token - end
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            print(new_password, 'is set')
            return Response({'message': 'Password reset successfully'}, status=200)
        return Response(serializer.errors, status=400)