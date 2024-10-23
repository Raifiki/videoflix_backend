from django.db import models
import uuid
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from content.utils import get_video_upload_path, get_video_thumbnail_path

# Create your models here.
class Video(models.Model):
    """ Class that descripts the Video model with the following fieds:
    uuid, title, description, genre, video, database_created and thumbnail"""
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.ForeignKey('Genre', on_delete = models.SET_NULL, null=True, blank=True)
    video = models.FileField(upload_to=get_video_upload_path, blank=True, null=True)
    database_created = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to=get_video_thumbnail_path, blank=True, null=True)
    

    
class Genre(models.Model):
    """ Class that descripts the Genre model with the following fieds: name"""
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name