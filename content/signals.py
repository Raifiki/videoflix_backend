



import os
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save, post_save

from content.models import Video
from content.utils import generate_and_store_thumbnail
from videoflix.settings import MEDIA_ROOT

@receiver(post_delete, sender=Video)
def delete_media_files_on_delete(sender, instance=None, created=False, **kwargs):
    if instance.video:
        instance.video.storage.delete(instance.video.name)
    if instance.thumbnail:
        instance.thumbnail.storage.delete(instance.thumbnail.name)
    
@receiver(pre_save, sender=Video)
def delete_media_files_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_video = Video.objects.get(pk=instance.pk).video
    except Video.DoesNotExist:
        return False
    if not old_video == instance.video:
        if old_video:
            os.remove(old_video.path)
        if instance.thumbnail:
            instance.thumbnail.storage.delete(instance.thumbnail.name)
            instance.thumbnail = None
        
            
@receiver(post_save, sender=Video)
def generate_thumbnail(sender, instance=None, created=False, **kwargs):
    if not instance.thumbnail:
        thumbnail_path = os.path.join('thumbnails/Video_'+ str(instance.pk) + '_Thumbnail.jpg')
        generate_and_store_thumbnail(instance.video.path, MEDIA_ROOT + '/' + thumbnail_path)
        instance.thumbnail = thumbnail_path
        instance.save()