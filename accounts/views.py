from django.http import request
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import Sign_Up_Form, Sign_In_Form, Profile_Update_Form, Social_Profile_Update_Form, Password_Change_Form, Contact_Group_Create_Form, Delete_Account_Form
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import SocialProfile, CustomUser
from chats.views import chat_base

def Sign_Up(request):
    form = Sign_Up_Form(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            user = authenticate(email=form.cleaned_data.get('email'), password=form.cleaned_data.get('password1'))
            login(request, user)
            return redirect('chat:index')
    return render(request, 'signup.html', {'form':form})

def Sign_In(request):
    form = Sign_In_Form(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('chat:index')
    return render(request, 'signin.html', {'form':form})

def Sign_Out(request):
    logout(request)
    return redirect('account:sign-in')

@login_required
def Settings(request):
    chat_context = chat_base(request)
    profile_form = Profile_Update_Form(instance=request.user)
    social_form = Social_Profile_Update_Form(instance=request.user.socialprofile)
    password_form = Password_Change_Form(user=request.user)
    delete_account_form = Delete_Account_Form()
    if request.method == 'POST':
        if 'profile-form' in request.POST:
            profile_form = Profile_Update_Form(request.POST, request.FILES, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
        if 'social-form' in request.POST:
            social_form = Social_Profile_Update_Form(request.POST, instance=request.user.socialprofile)
            if social_form.is_valid():
                social_form.save()
        if 'password-form' in request.POST:
            password_form = Password_Change_Form(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
        if 'group-form' in request.POST:
            group_form = Contact_Group_Create_Form(request.POST, request.FILES)
            if group_form.is_valid():
                temp = group_form.save(user=request.user)
                temp.members.add(request.user)
                for slug in request.POST.getlist('member'):
                    temp.members.add(CustomUser.objects.get(slug=slug))  
        if 'captcha-form' in request.POST:
            delete_account_form = Delete_Account_Form(request.POST)
            if delete_account_form.is_valid():
                user = authenticate(email=request.user.email, password=delete_account_form.cleaned_data.get('password'))
                if user:
                    user.delete()
                    return redirect('account:sign-up')
    context = {'profile_form':profile_form, 'password_form':password_form, 'social_form':social_form, 'delete_account_form':delete_account_form}
    context.update(chat_context)
    return render(request, 'settings.html', context)