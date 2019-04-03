from django.contrib.auth.signals import user_logged_out
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models


def show_message(sender, user, request, **kwargs):
    # whatever...
    messages.info(request, f'Good to see you {User.username}. See you soon!')
    user_logged_out.connect(show_message)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    currentlocation = models.CharField(max_length=50, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()