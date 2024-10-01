from django.contrib import admin

from content.models import Genre, Video

# Register your models here.
class AdminVideo(admin.ModelAdmin):
    list_display = [
        'uuid',
        'title',
        'description',
        ] 
    readonly_fields = ('thumbnail','database_created','uuid')
    
admin.site.register(Video, AdminVideo)

class AdminGenre(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        ] 
    
admin.site.register(Genre, AdminGenre)