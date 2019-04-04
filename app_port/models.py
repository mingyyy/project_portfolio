from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    # default: somewhere in the world
    currentlocation = models.CharField(max_length=50, blank=True)
    # ready or not to publish
    ready=models.BooleanField(default=False)


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Project(models.Model):
    userID=models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=False, blank=False)
    name=models.CharField(max_length=120,null=False)
    description=models.TextField()
    url=models.URLField()


class Tag(models.Model):
    category=models.CharField(max_length=50, null=False)
    name=models.CharField(max_length=50,null=False)
    users=models.ManyToManyField(User)


class Channel(models.Model):
    name=models.CharField(max_length=100,null=False)
    url=models.URLField()

class Selected(models.Model):
    name=models.CharField(max_length=50,null=False)