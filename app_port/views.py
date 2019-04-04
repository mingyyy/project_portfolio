from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.contrib import messages
from .models import Profile, Project, Tag, Channel
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Project, Channel, Tag
from django.core.files.storage import FileSystemStorage

@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    messages.add_message(request, messages.INFO, 'Logged out.')



def main(request):
    prof=Profile.objects.all()
    pj=Project.objects.all()
    tag=Tag.objects.all()
    choices={}
    if request.method == 'POST':
        for k, v in request.POST.items():
            if k != 'csrfmiddlewaretoken':
                if not 'tag' in request.session or not request.session['tag']:
                    request.session['tag'] = [v]
                else:
                    saved_list = request.session['tag']
                    saved_list.append(v)
                    request.session['tag'] = saved_list

        selected=request.session['tag']
        selected=set(selected)
        choices={"choices":selected}
    context={"profile":prof, "project":pj, "tags":tag, "choices":choices}
    return render(request, 'main.html', context)


def profile(request, user_id):
    prof=Profile.objects.get(id=user_id)
    pj=Project.objects.get(id=user_id)
    tag=Tag.objects.get(id=user_id)
    channel=Channel.objects.get(id=user_id)
    context={"profile":prof, "project":pj, "tag":tag, "channel":channel}
    return render(request, "profile.html")


@login_required
def edit(request):
    context = {}
    user = request.user
    if request.method == 'POST':
        print(request.FILES)
        if "save_profile" in request.POST:
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.profile.bio = request.POST["bio"]
            user.save()

            for key in request.POST.keys():
                if key[0:4] == "chan":
                    channelID = int(key[4:])
                    channel = Channel.objects.get(id=channelID)
                    channel.name = request.POST.getlist(key)[0]
                    channel.url = request.POST.getlist(key)[1]
                    channel.save()
                elif key[0:4] == "proj":
                    projectID = int(key[4:])
                    project = Project.objects.get(id=projectID)
                    project.name = request.POST.getlist(key)[0]
                    project.url = request.POST.getlist(key)[1]
                    project.description = request.POST.getlist(key)[2]
                    project.save()
                elif request.POST[key] != "":
                    user.profile.picture = request.FILES
                    user.save()

        elif "delete_items" in request.POST:
            delete_list= request.POST.getlist("delete")
            for item in delete_list:
                if item[0:4] == "proj":
                    projectID = int(item[4:])
                    Project.objects.filter(id=projectID).delete()
                elif item[0:4] == "chan":
                    channelID = int(item[4:])
                    Channel.objects.filter(id=channelID).delete()

        elif "channel_new" in request.POST:
            Channel.objects.create(name="Channel name", url="www.your-url-goes-here.com", userID=user)

        elif "project_new" in request.POST:
            Project.objects.create(name="New Project Title", description="Type your description here.", userID=user,
                                   url = "www.your-url-goes-here.com")
        elif request.FILES['picture']:
            print(123)
            picture = request.FILES['picture']
            user.profile.picture = picture
            user.save()



    channels = Channel.objects.filter(userID=user.id)
    projects = Project.objects.filter(userID=user.id)
    tags = user.tag_set.all()

    context["channels"]=channels
    context["projects"]=projects
    context["user"]=user
    context["tags"]=tags

    return render(request, "edit.html", context)


