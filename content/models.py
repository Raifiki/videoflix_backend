from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.ForeignKey('Genre', on_delete = models.SET_NULL, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails', blank=True, null=True)
    video = models.FileField(upload_to='videos', blank=True, null=True)
    
class Genre(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name