

from content.models import Genre, Video
from rest_framework import serializers

class GenreSerializer(serializers.ModelSerializer):
    """ Serializer for Genre model """
    class Meta:
        model = Genre
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    """ Serializer for Video model """
    genre = GenreSerializer( read_only=True)
    class Meta:
        model = Video
        fields = '__all__'
    
