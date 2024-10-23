from django.contrib import admin

from content.models import Genre, Video

# Register your models here.
class AdminVideo(admin.ModelAdmin):
    """ Class to display Video model in admin panel with uuid, title and description"""
    list_display = [
        'uuid',
        'title',
        'description',
        ] 
    readonly_fields = ('thumbnail','database_created','uuid')
    
admin.site.register(Video, AdminVideo)

class AdminGenre(admin.ModelAdmin):
    """ Class to display Genre model in admin panel with id and name"""
    list_display = [
        'id',
        'name',
        ] 
    
admin.site.register(Genre, AdminGenre)