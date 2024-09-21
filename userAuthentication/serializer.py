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
        
