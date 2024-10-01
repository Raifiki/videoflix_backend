from urllib import response
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from content.models import Genre, Video
from content.serializer import GenreSerializer, VideoSerializer
from rest_framework.response import Response

from rest_framework.views import APIView
# Create your views here.

class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]
    
class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated]
    
    
class secureFileView(APIView):
    permission_classes = []#[IsAuthenticated]
    #ToDo: Problem: Videoplayer from Frontend dont have the possibility to send tokens. 
    def get(self, request,path):
        file = 'media/' + path
        with open(file, 'rb') as f:
            content_type = 'video/mp4' if path.endswith('mp4') else 'image/png'
            response = HttpResponse(f.read(), content_type=content_type)
            response['Content-Disposition'] = 'inline; filename="video_file.mp4"'
            return response