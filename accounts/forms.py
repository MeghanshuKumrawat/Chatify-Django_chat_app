from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.db.models import fields
from django_countries import widgets
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from captcha.fields import CaptchaField
from .models import CustomUser, SocialProfile
from chats.models import Contact, Contact_Group, Stories, Story_image
import random, string

def rand_slug():
    slug = ''
    for _ in range(3):
        for i in range(5):
            char = random.choice(string.ascii_letters + string.digits) 
            slug += ''.join(char)
        if _ == 2:
            continue
        slug += '-'
    return slug

class Sign_Up_Form(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg', 'placeholder':'Enter your name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control form-control-lg', 'placeholder':'Enter your email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg', 'placeholder':'Enter your password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg', 'placeholder':'Confirm your password'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commmit=True):
        user = super(Sign_Up_Form, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.slug = rand_slug()
        if commmit:
            user.save()
        return user

class Sign_In_Form(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control form-control-lg', 'placeholder':'Email address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg', 'placeholder':'Password'}))

class Profile_Update_Form(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg', 'placeholder':'Username'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg', 'placeholder':'First name'}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg', 'placeholder':'Last name'}), required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control form-control-lg', 'placeholder':'you@yoursite.com'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg', 'placeholder':'9258454845'}), required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control form-control-lg', 'placeholder':'Express yourself', 'rows':4}), required=False)
    country = CountryField().formfield(widget=CountrySelectWidget(attrs={'class':'form-control form-control-lg', 'placeholder':'Country'}), required=False)
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'id':'upload-user-photo', 'class':'d-none'}))
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'country', 'bio', 'avatar']

class Social_Profile_Update_Form(forms.ModelForm):
    twitter = forms.URLField(widget=forms.URLInput(attrs={'class':'form-control form-control-lg', 'placeholder':'URL'}), required=False)
    facebook = forms.URLField(widget=forms.URLInput(attrs={'class':'form-control form-control-lg', 'placeholder':'URL'}), required=False)
    instagram = forms.URLField(widget=forms.URLInput(attrs={'class':'form-control form-control-lg', 'placeholder':'URL'}), required=False)
    github = forms.URLField(widget=forms.URLInput(attrs={'class':'form-control form-control-lg', 'placeholder':'URL'}), required=False)
    slack = forms.URLField(widget=forms.URLInput(attrs={'class':'form-control form-control-lg', 'placeholder':'URL'}), required=False)
    class Meta:
        model = SocialProfile
        fields = ['twitter', 'facebook', 'instagram', 'github', 'slack']

class Password_Change_Form(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg', 'placeholder':'Current password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg', 'placeholder':'New password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg', 'placeholder':'Verify password'}))

class Contact_Group_Create_Form(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'id':'upload-chat-photo', 'class':'d-none'}), required=False)
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg', 'placeholder':'Group Name'}))
    topic = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg', 'placeholder':'Group Topic'}), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control form-control-lg', 'placeholder':'Group Description', 'rows':4}))
    class Meta:
        model = Contact_Group
        fields = ['avatar', 'name', 'topic', 'description']
        
    
    def save(self, commit=True):
        group = super(Contact_Group_Create_Form, self).save(commit=False)
        if commit:
            group.save()
        return group

class Story_Image_Create_Form(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'id':'upload-story-photo', 'class':'d-none'}))
    caption = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg', 'placeholder':'Caption'}), required=False)
    class Meta:
        model = Story_image
        fields = ['image', 'caption']

class Delete_Account_Form(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg', 'placeholder':'Enter your password'}))
    captcha = CaptchaField()

class Captcha_Form(forms.Form):
    captcha = CaptchaField()

class Password_Form(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg', 'placeholder':'Enter your password'}))
