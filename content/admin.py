from django.contrib import admin

from content.models import Video

# Register your models here.
class AdminVideo(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'description',
        ] 
    
admin.site.register(Video, AdminVideo)