from django.contrib import admin

from userAuthentication.models import CustomUser

# Register your models here.

class AdminCustomUser(admin.ModelAdmin):
    """ Class to display CustomUser model in admin panel with id, email, password, is_active, is_superuser and is_staff """
    list_display = [
        'id',
        'email',
        'password',
        'is_active',
        'is_superuser',
        'is_staff',
        ] 
    
admin.site.register(CustomUser, AdminCustomUser)
