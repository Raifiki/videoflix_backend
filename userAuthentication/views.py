from urllib import request
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
from userAuthentication.serializer import CustomUserSerializer
from django.contrib.auth.tokens import default_token_generator

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