from urllib import request
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
#imports for rest framework
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

from userAuthentication.authentication import EmailVerificationAuthentication, LoginCustomUserAuthentication, ResetPasswordTokenAuthentication
from userAuthentication.models import CustomUser
from userAuthentication.serializer import CreateCustomUserSerializer, CustomUserSerializer, PasswordResetConfirmSerializer, PasswordResetSerializer
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator

from django.core.mail import send_mail
from django.template.loader import render_to_string

from videoflix.settings import FRONTEND_BASE_URL

# Create your views here.
class UserView(APIView):
    serializer_class = CustomUserSerializer
    
    def post(self, request):
        serializer = CreateCustomUserSerializer(data = request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = CustomUser.objects.create_user(email, password)
            respData = CustomUserSerializer(user).data
            return  Response(respData, content_type='application/json')
        return Response(serializer.errors, status=400)
    
# ToDo: Eventuell UserView, ResetPwd und VerifyEmail in ein Viewset mit create und put Methoden 


class VerifyEmailView(APIView):
    authentication_classes = [EmailVerificationAuthentication]
    def get(self, request):
        user = request.user
        user.is_active = True
        user.save()
        redirect_url = FRONTEND_BASE_URL + '/Login?email=' + user.email
        return HttpResponseRedirect(redirect_url)
    
class LoginView(ObtainAuthToken):
    authentication_classes = [LoginCustomUserAuthentication]
    def post(self, request):
        user = request.user
        respData = CustomUserSerializer(user).data
        return Response(respData, content_type='application/json')
    
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
        mail = 'leonard_weiss@web.de'# ToDo: change email to: email
        from_mail = 'django@demomailtrap.com' # ToDo: change email to domain email
        token = self._generate_password_reset_token(user)
        subject = 'Reset your Password'
        context = {
            'username': mail.split('@')[0],
            'reset_pwd_url': FRONTEND_BASE_URL + '/ResetPassword/?user_id=' + str(user.pk) + '&token=' + token
        }
        text_content = 'Hello ' + context['username'] + ', \n Please reset your password: ' + context['reset_pwd_url']
        html_content = render_to_string('reset_pwd_email.html', context)
        send_mail(subject, text_content, from_mail, [mail], html_message=html_content)
        
    def _generate_password_reset_token(self, user):
        token_generator=PasswordResetTokenGenerator()
        return token_generator.make_token(user)
        
class ResetPasswordConfirmView(APIView):
    authentication_classes = [ResetPasswordTokenAuthentication]
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            self._change_password(request.user, new_password)
            return Response({'email': request.user.email}, status=200)
        return Response(serializer.errors, status=400)
    
    def _change_password(self, user, new_password):
        user.set_password(new_password)
        user.save()