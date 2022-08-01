from django.contrib import admin
from .models import Contact, Contact_Group, Message, Stories, Story_image, Export_chat, Export_user_chat

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['user', 'friend','room']

@admin.register(Contact_Group)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['admin', 'name', 'room']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'message', 'forwarded']

@admin.register(Stories)
class StoriesAdmin(admin.ModelAdmin):
    list_display = ['user']

@admin.register(Story_image)
class StoriesAdmin(admin.ModelAdmin):
    list_display = ['story', 'image', 'caption']

@admin.register(Export_chat)
class Export_chatAdmin(admin.ModelAdmin):
    list_display = ['user', 'file', 'timestamp', 'room']

@admin.register(Export_user_chat)
class Export_user_chatAdmin(admin.ModelAdmin):
    list_display = ['user', 'file', 'timestamp', 'slug']