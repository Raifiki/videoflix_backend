from django.contrib import admin

from userAuthentication.models import CustomUser

# Register your models here.

class AdminCustomUser(admin.ModelAdmin):
    list_display = [
        'id',
        'email',
        'password',
        ] 
    
admin.site.register(CustomUser, AdminCustomUser)
