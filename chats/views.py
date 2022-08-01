from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.conf import settings
from accounts.forms import Contact_Group_Create_Form, Story_Image_Create_Form, Captcha_Form, rand_slug
from accounts.models import CustomUser
from .models import Contact, Contact_Group, Message, Stories, Story_image, Export_chat, Export_group_chat, Export_user_chat
import os

def chat_base(request):
    all_private_users = Contact.objects.filter(user=request.user)
    all_private_chats = Contact.objects.filter(user=request.user, chat=True, block=False)
    all_groups_chats = Contact_Group.objects.filter(members=request.user)
    
    default_message = get_object_or_404(Message, room='default')
    private_last_chats = []
    group_last_chats = []

    for private_chat in all_private_chats:
        message = Message.objects.filter(room=private_chat.room).last()
        private_last_chats.append(message if message else default_message)
    
    for group_chat in all_groups_chats:
        message = Message.objects.filter(room=group_chat.room).last()
        group_last_chats.append(message if message else default_message)

    group_create_form = Contact_Group_Create_Form()
    stories_create_form = Story_Image_Create_Form()
    captcha_form = Captcha_Form()

    context = {'all_private_chats':zip(all_private_chats, private_last_chats),
                'all_groups_chats':zip(all_groups_chats, group_last_chats),
                'all_private_users':all_private_users,
                'all_groups':all_groups_chats,
                'group_create_form':group_create_form,
                'stories_create_form':stories_create_form,
                'captcha_form':captcha_form}
    return context

# --------------------------------------------index--------------------------------------

@login_required
def index(request):
    chat_context = chat_base(request)
    context = {}
    context.update(chat_context)
    return render(request, 'index.html', context)

# ---------------------------------------------room-----------------------------------------

def single_chat_room(request, room):
    user_private_chat = get_object_or_404(Contact, user=request.user, room=room, chat=True, block=False)
    messages = Message.objects.filter(room=room).order_by('timestamp')
    chat_context = chat_base(request)
    context = {'room':room, 'user_private_chat':user_private_chat, 'messages':messages}
    context.update(chat_context)
    return render(request, 'chat-2.html', context)

def group_chat_room(request, room):
    user_group_chat = get_object_or_404(Contact_Group, members=request.user, room=room)
    messages = Message.objects.filter(room=room).order_by('timestamp')
    group_edit_form = Contact_Group_Create_Form(instance=user_group_chat)
    chat_context = chat_base(request)
    context = {'room':room, 'user_group_chat':user_group_chat, 'messages':messages, 'group_edit_form':group_edit_form,}
    context.update(chat_context)
    return render(request, 'chat-1.html', context)

#--------------------------------------------story-------------------------------------------

def stories_view(request, slug):
    user = get_object_or_404(CustomUser, slug=slug)
    story_user = get_object_or_404(Stories ,user=user)
    stories = Story_image.objects.filter(story=story_user)
    if request.user != story_user.user:
        story_user.seen.add(request.user)
    chat_context = chat_base(request)
    context = {'stories':stories, 'story_user':story_user}
    context.update(chat_context)
    return render(request, 'stories.html', context)

def create_group(request):
    if request.method == 'POST':
        if 'group-form' in request.POST:
            group_form = Contact_Group_Create_Form(request.POST, request.FILES)
            if group_form.is_valid():
                temp = group_form.save(commit=False)
                temp.admin = request.user
                temp.room = rand_slug()
                temp.save()
                temp.members.add(request.user)
                for slug in request.POST.getlist('member'):
                    temp.members.add(CustomUser.objects.get(slug=slug))    
                return redirect('chat:group-chat-room', room=temp.room)
    else:
        return HttpResponseForbidden()

def edit_group(request):
    if request.method == 'POST' and 'group-edit-form' in request.POST:
        room = request.POST.get('group-edit-form')
        group = get_object_or_404(Contact_Group, room=room)
        group_form = Contact_Group_Create_Form(request.POST, request.FILES, instance=group)
        if group_form.is_valid():
            group_form.save()
            return redirect('chat:group-chat-room', room=group.room)
    else:
        return HttpResponseForbidden()

def create_stories(request):
    if request.method == 'POST' and 'create-stories' in request.POST:
        form = Story_Image_Create_Form(request.POST, request.FILES)
        if form.is_valid():
            temp = form.save(commit=False)
            temp_stories, _ = Stories.objects.get_or_create(user=request.user)
            temp.story = temp_stories
            temp.save()
        return redirect('chat:index')
    else:
        return HttpResponseForbidden()

def delete_stories(request):
    stories = request.POST.get('images')
    for pk in stories:
        temp = get_object_or_404(Story_image, id=pk)
        temp.delete()
    return redirect('chat:index')

def start_chat(request, room):
    contact = get_object_or_404(Contact, user=request.user, room=room)
    if contact:
        contact.chat = True
        contact.save()
        return redirect('chat:single-chat-room', room=room)
    else:
        return HttpResponseForbidden()

def add_close_friend(request, room):
    """ Feature : Add to close friends """
    contact = get_object_or_404(Contact, user=request.user, room=room)
    contact.close_friend = True
    contact.save()
    return redirect('chat:single-chat-room', room=contact.room)

def remove_close_friend(request, room):
    """ Feature : Remove from close friends """
    contact = get_object_or_404(Contact, user=request.user, room=room)
    contact.close_friend = False
    contact.save()
    return redirect('chat:single-chat-room', room=contact.room)

def clear_chat(request, room):
    """ Feature : Clear all messages of one chat """
    chats = Message.objects.filter(room=room)
    chats.delete()
    return redirect('chat:single-chat-room', room=room)

def clear_all_chat(request):
    """ Feature : Clear all messages of one chat """
    chats = Message.objects.filter(user=request.user)
    chats.delete()
    return redirect('account:settings')

def delete_chat(request, room):
    contact = get_object_or_404(Contact, user=request.user, room=room)
    if contact:
        chats = Message.objects.filter(room=contact.room)
        chats.delete()
        contact.delete()
        return redirect('chat:index')
    else:
        return HttpResponseForbidden()

def delete_all_chat(request):
    contacts = Contact.objects.filter(user=request.user)
    for contact in contacts:
        chats = Message.objects.filter(room=contact.room)
        chats.delete()
        contact.delete()
        return redirect('chat:index')
    else:
        return HttpResponseForbidden()

def block_user(request, room):
    contact = get_object_or_404(Contact, user=request.user, room=room)
    if contact:
        contact.block = True
        contact.save()
        return redirect('chat:index')
    else:
        return HttpResponseBadRequest()

def unblock_user(request, room):
    contact = get_object_or_404(Contact, user=request.user, room=room)
    if contact:
        contact.block = False
        contact.save()
        return redirect('chat:index')
    else:
        return HttpResponseBadRequest()

def message_delete_for_everyone(request, chat_type, pk):
    msg = get_object_or_404(Message, pk=pk)
    if msg.user == request.user:
        msg.delete()
        if chat_type == 'group':
            return redirect('chat:group-chat-room', room=msg.room)
        elif chat_type == 'single':
            return redirect('chat:single-chat-room', room=msg.room)
    else:
        return HttpResponseForbidden()

def message_delete_for_me(request, chat_type, pk):
    msg = get_object_or_404(Message, id=pk)
    msg.delete_by.add(request.user)
    if chat_type == 'group':
            return redirect('chat:group-chat-room', room=msg.room)
    elif chat_type == 'single':
        return redirect('chat:single-chat-room', room=msg.room)
    else:
        return HttpResponseForbidden()

def forward_message(request):
    if request.method == 'POST':
        msg = get_object_or_404(Message, pk=request.POST.get('forward-chat'))
        for room in request.POST.getlist('member'):
            Message.objects.create(user=request.user, room=room, message=msg, forwarded=True)
        if Contact.objects.filter(room=msg.room).exists():
            return redirect('chat:single-chat-room', room=msg.room)
        else:
            return redirect('chat:group-chat-room', room=msg.room)
    return HttpResponseForbidden()

def add_to_group(request, room):
    group = get_object_or_404(Contact_Group, room=room)
    if request.method == 'POST' and group.admin == request.user:
        for slug in request.POST.getlist('member'):
            group.members.add(CustomUser.objects.get(slug=slug))  
        return redirect('chat:group-chat-room', room=room)
    return HttpResponseForbidden()

def remove_from_group(request, room, slug):
    group = get_object_or_404(Contact_Group, room=room)
    user = get_object_or_404(CustomUser, slug=slug)
    if group.admin == user:
        group.members.remove(user)
        return redirect('chat:index')
    elif group.admin == request.user:
        group.members.remove(user)
        return redirect('chat:group-chat-room', room=room)
    elif user == request.user:
        group.members.remove(user)
        return redirect('chat:index')
    return HttpResponseForbidden()

def export_chat(request, room):
    """ Feature : Export a single person chat """
    user = get_object_or_404(Contact, user=request.user, room=room)
    chats = Message.objects.filter(room=user.room)
    temp_file, created = Export_chat.objects.get_or_create(user=user, room=user.room)
    if created:
        txt_file = open(settings.FILE_PATH+'\\'+user.friend.username+'-'+user.user.username+'.txt', 'w')
        for chat in chats:
            txt_file.write(str(chat.timestamp.strftime("%d-%b-%Y, %H:%M:%S")) + ' - ' + chat.user.username + ' : ' + chat.message + '\n')
        temp_file.file = 'exported_files/'+user.friend.username+'-'+user.user.username+'.txt' #File(txt_file, name=os.path.basename(txt_file.name))
        temp_file.save()
        txt_file.close()
    else:
        txt_file = open(temp_file.file.path, 'w')
        for chat in chats:
            txt_file.write(str(chat.timestamp.strftime("%d-%b-%Y, %H:%M:%S")) + ' - ' + chat.user.username + ' : ' + chat.message + '\n')
        txt_file.close()

    return redirect('chat:export-chat-preview', pk=temp_file.id)

def export_chat_preview(request, pk):
    """ Feature : See preview of your exported document for one chat """
    file = get_object_or_404(Export_chat, id=pk)
    data = open(file.file.path, 'r').readlines()
    chat_context = chat_base(request)
    context = {'data':data, 'file':file, 'type':'single'}
    context.update(chat_context)
    return render(request, 'export-preview.html', context)

def download_chat_file(request, pk):
    """ Feature : Download your exported file in .txt format for one chat """
    file = get_object_or_404(Export_chat, id=pk)
    file_path = file.file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fi:
            response = HttpResponse(fi.read(), content_type="application/vnd.ms-word")
            response['Content-Disposition'] = 'inline; filename='+os.path.basename(file_path)
            return response
        raise response.Http404

def export_group_chat(request, room):
    """ Feature : Export a single person chat """
    group = get_object_or_404(Contact_Group, room=room)
    chats = Message.objects.filter(room=group.room)
    temp_file, created = Export_group_chat.objects.get_or_create(group=group, room=group.room)
    if created:
        txt_file = open(settings.FILE_PATH+'\\'+group.name+'-'+request.user.username+'.txt', 'w')
        for chat in chats:
            txt_file.write(str(chat.timestamp.strftime("%d-%b-%Y, %H:%M:%S")) + ' - ' + chat.user.username + ' : ' + chat.message + '\n')
        temp_file.file = 'exported_files/'+group.name+'-'+request.user.username+'.txt' #File(txt_file, name=os.path.basename(txt_file.name))
        temp_file.save()
        txt_file.close()
    else:
        txt_file = open(temp_file.file.path, 'w')
        for chat in chats:
            txt_file.write(str(chat.timestamp.strftime("%d-%b-%Y, %H:%M:%S")) + ' - ' + chat.user.username + ' : ' + chat.message + '\n')
        txt_file.close()

    return redirect('chat:export-group-chat-preview', pk=temp_file.id)

def export_group_chat_preview(request, pk):
    """ Feature : See preview of your exported document for one chat """
    file = get_object_or_404(Export_group_chat, id=pk)
    data = open(file.file.path, 'r').readlines()
    chat_context = chat_base(request)
    context = {'data':data, 'file':file, 'type':'group'}
    context.update(chat_context)
    return render(request, 'export-preview.html', context)

def download_group_chat_file(request, pk):
    """ Feature : Download your exported file in .txt format for one chat """
    file = get_object_or_404(Export_group_chat, id=pk)
    file_path = file.file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fi:
            response = HttpResponse(fi.read(), content_type="application/vnd.ms-word")
            response['Content-Disposition'] = 'inline; filename='+os.path.basename(file_path)
            return response
        raise response.Http404

def export_all_chats(request):
    """ Feature : Export all chats related to your account """
    peoples = Contact.objects.filter(user=request.user)
    groups = Contact_Group.objects.filter(members=request.user)
    temp_file, created = Export_user_chat.objects.get_or_create(user=request.user)
    if created:
        txt_file = open(settings.FILE_PATH+'\\'+request.user.username+'_all_chats.txt', 'w')
        for people in peoples:
            chats = Message.objects.filter(room=people.room).order_by('timestamp')
            txt_file.write(people.user.username + ' and ' + people.friend.username + '\n' + '----------------------------------------\n')
            for chat in chats:
                txt_file.write(str(chat.timestamp.strftime("%d-%b-%Y, %H:%M:%S")) + ' - ' + chat.user.username + ' : ' + chat.message + '\n')
            txt_file.write('\n')
        for group in groups:
            chats = Message.objects.filter(room=group.room).order_by('timestamp')
            txt_file.write(group.name + '\n' + '----------------------------------------\n')
            for chat in chats:
                txt_file.write(str(chat.timestamp.strftime("%d-%b-%Y, %H:%M:%S")) + ' - ' + chat.user.username + ' : ' + chat.message + '\n')
            txt_file.write('\n')
        txt_file.close()
        temp_file.file = 'exported_files/'+request.user.username+'_all_chats.txt'
        temp_file.slug = rand_slug()
        temp_file.save()
    else:
        txt_file = open(temp_file.file.path, 'w')
        for people in peoples:
            chats = Message.objects.filter(room=people.room).order_by('timestamp')
            txt_file.write(people.user.username + ' and ' + people.friend.username + '\n' + '----------------------------------------\n')
            for chat in chats:
                txt_file.write(str(chat.timestamp.strftime("%d-%b-%Y, %H:%M:%S")) + ' - ' + chat.user.username + ' : ' + chat.message + '\n')
            txt_file.write('\n\n')
        for group in groups:
            chats = Message.objects.filter(room=group.room).order_by('timestamp')
            txt_file.write(group.name + '\n' + '----------------------------------------\n')
            for chat in chats:
                txt_file.write(str(chat.timestamp.strftime("%d-%b-%Y, %H:%M:%S")) + ' - ' + chat.user.username + ' : ' + chat.message + '\n')
            txt_file.write('\n')
        txt_file.close()
    return redirect('chat:export-all-chat-preview', pk=temp_file.pk)

def export_all_chats_preview(request, pk):
    """ Feature : See preview of your exported document """
    file = get_object_or_404(Export_user_chat, id=pk)
    data = open(file.file.path, 'r').readlines()
    chat_context = chat_base(request)
    context = {'data':data, 'file':file}
    context.update(chat_context)
    return render(request, 'export-preview.html', context)

def download_all_chat_file(request, pk):
    """ Feature : Download your exported file in .txt format """
    file = get_object_or_404(Export_user_chat, id=pk)
    file_path = file.file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fi:
            response = HttpResponse(fi.read(), content_type="application/vnd.ms-word")
            response['Content-Disposition'] = 'inline; filename='+os.path.basename(file_path)
            return response
        raise response.Http404

def change_security_code(request, slug):
    user = get_object_or_404(CustomUser, slug=slug)
    if request.user == user:
        user.slug = rand_slug()
        user.save()
        return redirect('account:settings')
    else:
        return HttpResponseBadRequest()

def change_room_security_code(request, type, room):
    if type == 'single':
        temp = get_object_or_404(Contact, user=request.user, room=room)
        temp_2 = get_object_or_404(Contact, friend=request.user, room=room)
        if temp.user == request.user:
            slug = rand_slug()
            temp.room = slug
            temp.save()
            temp_2.room = slug
            temp_2.save()
            messages = Message.objects.filter(room=room)
            for message in messages:
                message.room = slug
                message.save()
            return redirect('chat:single-chat-room', room=temp.room)
        else:
            return HttpResponseBadRequest()
    elif type == 'group':
        temp = get_object_or_404(Contact_Group, room=room)
        if request.user in temp.members.all():
            slug = rand_slug()
            temp.room = slug
            temp.save()
            messages = Message.objects.filter(room=room)
            for message in messages:
                message.room = slug
                message.save()
            return redirect('chat:group-chat-room', room=temp.room)
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseForbidden()

def report(request, type, room):
    if type == 'single':
        contact = get_object_or_404(Contact, user=request.user, room=room)
        temp = get_object_or_404(CustomUser, slug=contact.friend.slug)
        if request.GET.get('block'):
            temp.report.add(request.user)
            temp.save()
            contact.block = True
            contact.save()
            chat = Message.objects.filter(room=contact.room)
            chat.delete()
            return redirect('chat:index')
        else:
            temp.report.add(request.user)
            temp.save()
            return redirect('chat:single-chat-room', room=contact.room)
    elif type == 'group':
        temp = get_object_or_404(Contact_Group, room=room)
        if request.GET.get('exit'):
            temp.report.add(request.user)
            temp.save()
            temp.members.remove(request.user)
            return redirect('chat:index')
        else:
            temp.report.add(request.user)
            temp.save()
            return redirect('chat:group-chat-room', room=temp.room)
    else:
        return HttpResponseForbidden()