from urllib import response
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from content.models import Genre, Video
from content.serializer import GenreSerializer, VideoSerializer
from rest_framework.response import Response

from rest_framework.views import APIView

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from videoflix.settings import CACHE_TTL

# Create your views here.

class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    """ Class to define the video viewset"""
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]
    
class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """ Class to define the genre viewset"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated]
    
   
class secureFileView(APIView):
    """ Class to define the secure file view, the file is stored in media folder and is cashed for 1 hour in redis cache"""
    permission_classes = []
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request,path):
        file = 'media/' + path
        with open(file, 'rb') as f:
            content_type = 'video/mp4' if path.endswith('mp4') else 'image/png'
            response = HttpResponse(f.read(), content_type=content_type)
            response['Content-Disposition'] = 'inline; filename="video_file.mp4"'
            return response