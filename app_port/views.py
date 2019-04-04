from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.contrib import messages
from .models import Profile, Project, Tag, Channel


@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    messages.add_message(request, messages.INFO, 'Logged out.')


def main(request):
    prof=Profile.objects.all()
    pj=Project.objects.all()
    tag=Tag.objects.all()
    choice_store=[]

    for k, v in request.POST.items():
        if k!='csrfmiddlewaretoken':
            choice_store.append(v)


    choices={"choices":choice_store}
    context={"profile":prof, "project":pj, "tags":tag, "choices":choices}
    return render(request, 'main.html', context)


def edit(request):
    return render(request, "edit.html")


def profile(request, user_id):
    prof=Profile.objects.get(id=user_id)
    pj=Project.objects.get(id=user_id)
    tag=Tag.objects.get(id=user_id)
    channel=Channel.objects.get(id=user_id)
    context={"profile":prof, "project":pj, "tag":tag, "channel":channel}
    return render(request, "profile.html")
