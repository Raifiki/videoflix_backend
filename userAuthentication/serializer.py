from rest_framework import serializers

from userAuthentication.models import CustomUser

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email']