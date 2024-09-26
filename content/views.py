from urllib import response
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from content.models import Genre, Video
from content.serializer import GenreSerializer, VideoSerializer
from rest_framework.response import Response
# Create your views here.

class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]
    
class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated]