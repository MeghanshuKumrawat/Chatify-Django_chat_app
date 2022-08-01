from django.db import models
from accounts.models import CustomUser

class Contact(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    friend = models.ForeignKey(CustomUser, related_name='friend', on_delete=models.CASCADE)
    room = models.CharField(max_length=25)
    chat = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(blank=True, null=True)
    block = models.BooleanField(default=False)
    close_friend = models.BooleanField(default=False)

    def __str__(self):
        return self.room

class Contact_Group(models.Model):
    admin = models.ForeignKey(CustomUser, related_name='admin', on_delete=models.CASCADE)
    members = models.ManyToManyField(CustomUser)
    avatar = models.ImageField(default="avatar.png", upload_to="group_avatars")
    name = models.CharField(max_length=50)
    topic = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField()
    report = models.ManyToManyField(CustomUser, related_name='reporters', blank=True)
    room = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.CharField(max_length=25)
    message = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    forwarded = models.BooleanField(default=False)
    delete_by = models.ManyToManyField(CustomUser, related_name='deleted_by', blank=True)
    def __str__(self):
        return self.message

class Stories(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    seen = models.ManyToManyField(CustomUser, related_name='seens')
    def __str__(self):
        return self.user.username

class Story_image(models.Model):
    story = models.ForeignKey(Stories, on_delete=models.CASCADE)
    image= models.ImageField(upload_to='stories')
    caption = models.CharField(max_length=200)
    def __str__(self):
        return self.story.user.username

class Export_chat(models.Model):
    user = models.ForeignKey(Contact, on_delete=models.CASCADE)
    file = models.FileField(upload_to='exported_files', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.CharField(max_length=25)

class Export_group_chat(models.Model):
    group = models.ForeignKey(Contact_Group, on_delete=models.CASCADE)
    file = models.FileField(upload_to='exported_files', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.CharField(max_length=25)
    
class Export_user_chat(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to='exported_files', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)