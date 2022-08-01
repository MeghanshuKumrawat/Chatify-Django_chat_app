from django.urls import path
from .views import *

app_name = 'chat'

urlpatterns = [
    path('', index, name='index'),
    path('private-room/<str:room>', single_chat_room, name='single-chat-room'),
    path('group-room/<str:room>', group_chat_room, name='group-chat-room'),
    path('view-stories/<str:slug>', stories_view, name='stories-view'),
    path('create-stories', create_stories, name='create-stories'),
    path('delete-stories', delete_stories, name='delete-stories'),
    path('create-group', create_group, name='create-group'),
    path('edit-group', edit_group, name='edit-group'),
    path('start-chat/<room>', start_chat, name='start-chat'),
    path('clear-chat/<room>', clear_chat, name='clear-chat'),
    path('clear-all-chat', clear_all_chat, name='clear-all-chat'),
    path('delete-chat/<room>', delete_chat, name='delete-chat'),
    path('delete-all-chat', delete_all_chat, name='delete-all-chat'),
    path('block-user/<room>', block_user, name='block-user'),
    path('unblock-user/<room>', unblock_user, name='unblock-user'),
    path('export-chat/<room>', export_chat, name='export-chat'),
    path('export-chat-preview/<pk>', export_chat_preview, name='export-chat-preview'),
    path('download-chat/<pk>', download_chat_file, name='download-chat'),
    path('export-group-chat/<room>', export_group_chat, name='export-group-chat'),
    path('export-group-chat-preview/<pk>', export_group_chat_preview, name='export-group-chat-preview'),
    path('download-group-chat/<pk>', download_group_chat_file, name='download-group-chat'),
    path('export-all-chat', export_all_chats, name='export-all-chat'),
    path('export-all-chat-preview/<pk>', export_all_chats_preview, name='export-all-chat-preview'),
    path('download-all-chat/<pk>', download_all_chat_file, name='download-all-chat'),
    path('delete-for-me/<chat_type>/<pk>', message_delete_for_me, name='delete-for-me'),
    path('delete-for-everyone/<chat_type>/<pk>', message_delete_for_everyone, name='delete-for-everyone'),
    path('forward-message', forward_message, name='forward-message'),
    path('add-to-group/<room>', add_to_group, name='add-to-group'),
    path('remove-from-group/<room>/<slug>', remove_from_group, name='remove-from-group'),
    path('add-close-friend/<room>', add_close_friend, name='add-close-friend'),
    path('remove-close-friend/<room>', remove_close_friend, name='remove-close-friend'),
    path('change-security-code/<slug>', change_security_code, name='change-security-code'),
    path('change-room-security-code/<type>/<room>', change_room_security_code, name='change-room-security-code'),
    path('report/<type>/<room>', report, name='report'),

]