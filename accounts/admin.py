from django.contrib import admin
from .models import CustomUser, SocialProfile

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_superuser', 'slug']

@admin.register(SocialProfile)
class SocialAdmin(admin.ModelAdmin):
    list_display = ['user', 'twitter', 'facebook', 'instagram', 'github', 'slack']