



import os
import shutil
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save, post_save

from content.models import Video
from content.utils import delete_folder_content, generate_and_store_thumbnail, generate_thumbnail_folder, convert_video_and_store, get_video_upload_path
from videoflix.settings import MEDIA_ROOT

@receiver(post_delete, sender=Video)
def delete_media_files_on_delete(sender, instance=None, created=False, **kwargs):
    if instance.video:
        video_database_folder = MEDIA_ROOT + '/videos/' + str(instance.uuid)
        shutil.rmtree(video_database_folder)
        
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
                
        
@receiver(post_save, sender=Video)
def generate_single_video_database(sender,instance=None, created=False, **kwargs):
    if not instance.database_created:
        res = [480, 720, 1080]
        for resolution in res: convert_video_and_store(instance.video.path, resolution)
        thumbnail_path = os.path.join('videos/' + str(instance.uuid) + '/thumbnail.jpg')
        generate_and_store_thumbnail(instance.video.path, MEDIA_ROOT + '/' + thumbnail_path)
        instance.thumbnail = thumbnail_path
        instance.database_created = True
        instance.save()