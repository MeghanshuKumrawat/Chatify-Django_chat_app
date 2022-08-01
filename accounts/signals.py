from django.db.models.signals import post_save
from .models import CustomUser, SocialProfile
from django.dispatch import receiver

@receiver(post_save, sender=CustomUser)
def create_social_profile(sender, instance, created, **kwargs):
    if created:
        SocialProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_social_profile(sender, instance, **kwargs):
    instance.socialprofile.save()