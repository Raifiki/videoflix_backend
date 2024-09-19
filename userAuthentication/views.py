from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from userAuthentication.models import CustomUser
from userAuthentication.serializer import UserSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    authentication_classes = []#[TokenAuthentication]
    
    def create(self, request, *args, **kwargs):
        if not self.validateData(request.data): return HttpResponse('Missing data', status=400)
        email, password, passwordConfirm = self.getData(request.data)
        if password != passwordConfirm: return HttpResponse('Passwords do not match', status=400)
        if CustomUser.objects.filter(email=email).exists(): return HttpResponse('Email already exists', status=400)
        user = CustomUser.objects.create_user('',email, password)
        respData = UserSerializer(user).data
        return  Response(respData, content_type='application/json')
    
    def validateData(self, data):
        return data.get('email') and data.get('password') and data.get('passwordConfirm')
    
    def getData(self, data):
        email = data.get('email')
        password = data.get('password')
        passwordConfirm = data.get('passwordConfirm')
        return email, password, passwordConfirm