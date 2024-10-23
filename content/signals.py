



import os
import shutil
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save, post_save

from content.models import Video
from content.utils import delete_folder_content, generate_and_store_thumbnail, convert_video_and_store, get_video_thumbnail_path
from videoflix.settings import MEDIA_ROOT

import django_rq
""" Signal that is called when a video is deleted --> If the the video is in database, the media files are deleted"""
@receiver(post_delete, sender=Video)
def delete_media_files_on_delete(sender, instance=None, created=False, **kwargs):
    if instance.video:
        video_database_folder = MEDIA_ROOT + '/videos/' + str(instance.uuid)
        shutil.rmtree(video_database_folder)
        
""" Signal that is called before a video is saved --> IF the video is in database and the video is changed, the media files are deleted"""
@receiver(pre_save, sender=Video)
def delete_media_files_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_video = Video.objects.get(pk=instance.pk).video
    except Video.DoesNotExist:
        return False
    if not old_video.name == instance.video.name:
        if old_video:
            delete_folder_content(MEDIA_ROOT + '/videos/' + str(instance.uuid))
            instance.thumbnail = None
            instance.database_created = False
       
         
""" Signal that is called after a video is saved --> If the video_database is not created, the media files wlll be created"""
@receiver(post_save, sender=Video)
def generate_single_video_database(sender,instance=None, created=False, **kwargs):
    if not instance.database_created:
        res = [480, 720, 1080]
        queue = django_rq.get_queue('default', autocommit=True)
        for resolution in res: queue.enqueue(convert_video_and_store, instance.video.path, resolution)
        thumbnail_path = get_video_thumbnail_path(instance)
        generate_and_store_thumbnail(instance.video.path, MEDIA_ROOT + '/' + thumbnail_path)
        instance.thumbnail = thumbnail_path
        instance.database_created = True
        instance.save()